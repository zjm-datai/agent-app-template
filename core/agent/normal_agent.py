



import logging
import re
from typing import Annotated, List, Literal, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import trim_messages as _trim_message
from langchain_core.messages import ToolMessage
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import END

from pydantic import Field, field_validator

from asyncio import graph
from core.agent.graph_agent_base import BaseGraphAgent
from models.base import BaseModel

from configs import config
from schemas.chat import Message

logger = logging.getLogger(__name__)

def dump_messages(messages: list[Message]) -> list[dict]:
    """Dump the messages to a list of dictionaries.

    Args:
        messages (list[Message]): The messages to dump.

    Returns:
        list[dict]: The dumped messages.
    """
    return [message.model_dump() for message in messages]

def prepare_message(messages: List[Message], llm: BaseChatModel, system_prompt: str) -> List[dict]:
    """Prepare the messages for the LLM."""

    # 对于 trim_message 这个方法来说要么给他 langchain 官方的消息类型的列表
    # 要么给它字典列表，但是每个字典要有相应的键，role content 都要有
    # trimmed = trim_messages(
    #     [
    #         {"role": "system", "content": "你好"},
    #         {"role": "user", "content": "今天天气怎样?"}
    #     ],
    #     token_counter=...,
    #     max_tokens=100
    # )

    trimmed_messages = _trim_message(
        dump_messages(messages),
        strategy="last",
        token_counter=llm,
        max_tokens=config.MAX_TOKENS,
        start_on="human",
        include_system=False,
        allow_partial=False    
    )

    return [Message(role="system", content=system_prompt)] + trimmed_messages

class GraphState(BaseModel):
    """state definition for the langgraph agent/worlflow."""

    messages: Annotated[list, add_messages] = Field(
        default_factory=list, description="The messages in the conversation"    
    )
    session_id: str = Field(..., description="The unique identifier for the conversation session")

    @field_validator("session_id")
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        """Validate that the session ID is valid UUID or follows safe pattern.
        
        Args:
            v: The thread ID to validate

        Returns:
            str: The validated session ID

        Raises:
            ValueError: If the session ID is not valid
        """
        try:
            pass 
        except ValueError:
            # If not a UUID, check for safe characters only
            if not re.match(r"^[a-zA-Z0-9_\-]+$", v):
                raise ValueError("Session ID must contain only alphanumeric characters, underscores, and hyphens")
            return v

class NormalAgent(BaseGraphAgent[GraphState]):
    """This is simple implement of base agent."""


    async def create_graph(self) -> Optional[CompiledStateGraph]:
        """Create and configure the LangGraph workflow."""

        if self._graph is None:
            try:

                graph_builder = StateGraph(GraphState)
                graph_builder.add_node("chat", self._chat)
                graph_builder.add_node("tool_call", self._tool_call)
                graph_builder.add_conditional_edges(
                    "chat",
                    self._should_continue,
                    {
                        "continue": "tool_call",
                        "end": END    
                    }    
                )
                graph_builder.add_edge("tool_call", "chat")
                graph_builder.set_entry_point("chat")
                graph_builder.set_finish_point("chat")

                # Get connection pool (may be None in production if DB unavailable)
                connection_pool = await self._get_connection_pool()
                if connection_pool:
                    checkpointer = AsyncPostgresSaver(connection_pool)
                    await checkpointer.setup()
                else:
                    # In production, proceed without checkpointer if needed
                    checkpointer = None
                    if config.ENVIRONMENT != Environment.PRODUCTION:
                        raise Exception("Connection pool initialization failed!")
                    
                self._graph = graph_builder.compile(
                    checkpointer=checkpointer, name=f"normal-agent-{config.ENVIRONMENT.value}"    
                )

                logger.info(
                    "graph created",
                    graph_name="normal-agent",
                    environment=config.ENVIRONMENT.value,
                    has_checkpoiner=checkpointer is not None    
                )

            except Exception as e:
                logger.error("graph_creation_failed", error=str(e), environment=config.ENVIRONMENT.value)
                # In production, we don't want to crash the app
                if config.ENVIRONMENT == Environment.PRODUCTION:
                    logger.warning("continuing_without_graph")
                    return None
                raise e
            
    async def _chat(self, state: GraphState):
        """Process the chat state and generate a response."""

        messages = prepare_message(state.messages, self.llm, SYSTEM_PROMPT)
        llm_calls_num = 0

        # Configure retry attempts based on env
        max_retries = config.MAX_LLM_CALL_RETRIES

        for attempt in range(max_retries):
            try:
                with llm_inference_duration_seconds.labels(model=self.llm.model_name).time():
                    generated_state = {
                        "message": [await self.llm.ainvoke(dump_messages(messages))]
                    }

                    return generated_state
            except OpenAIError as e:

                llm_calls_num += 1

                continue

            raise Exception(f"Failed to get a response from the LLM after {max_retries} attempts")
        
    # Define our tool node
    async def _tool_call(self, state: GraphState) -> GraphState:
        """Process tool calls from the last message."""

        outputs = []
        for tool_call in state.messages[-1].tool_calls:
            tool_result = await self.tools_by_name[tool_call["name"]].ainvoke(tool_call["args"])
            outputs.append(
                ToolMessage(
                    content=tool_result,
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"]    
                )    
            )
        
        return {
            "messages": outputs    
        }

    def _should_continue(self, state: GraphState) -> Literal["end", "continue"]:
        """Determine if the agent should continue or end based on the last message."""

        messages = state.messages
        last_message = messages[-1]
        # If there is no function call, then we finish
        if not last_message.tool_calls:
            return "end"
        else:
            return "continue"
        
    def _get_connection_pool(self, )