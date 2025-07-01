"""This file contains the LangGraph Agent/workflow and interactions with the LLMs."""

import logging
from abc import ABC, abstractmethod
from ast import Dict, List
from typing import Any, Literal, Optional

from langchain_openai import ChatOpenAI
from langgraph.graph.state import CompiledStateGraph
from psycopg_pool import AsyncConnectionPool

from configs import config
from models.base import BaseModel

logger = logging.getLogger(__name__)

class BaseGraphAgent(ABC):
    """Mananges the LangGraph Agent/Workflow and interactions with the LLM.
    
    This class handles the creation and management of the LangGraph workflow,
    including LLM interactions, database connections, and response processing.
    """
    
    def __init__(self, tools: List[Any]):
        """Initialize the langgraph agent with necessary components."""

        # use environment-specific LLM model
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=config.DEFAULT_LLM_TEMPERATURE,
            api_key=config.LLM_API_KEY,
            base_url=config.LLM_BASE_URL,
            max_tokens=config.MAX_TOKENS,
            **self._get_model_kwargs(),
        ).bind_tools(tools)

        self.tools_by_name = {
            tool.name for tool in tools    
        }
        self._connection_pool: Optional[AsyncConnectionPool] = None
        self._graph: Optional[CompiledStateGraph]

        logger.info("llm_initialized", model=config.LLM_MODEL)

    def get_model_kwargs(self) -> Dict[str, Any]:
        pass 

    @abstractmethod
    async def create_graph(self) -> Any:
        """Construct and compile the workflow graph."""

        raise NotImplementedError("Subclasses must implement create_graph method")
    






