from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class BaseModel(SQLModel):
    """
    Base model with common fields.
    不带 table=True，不会自己生成表。
    """
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description="记录创建时间，UTC 时区"
    )