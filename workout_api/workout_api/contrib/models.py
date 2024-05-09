import uuid

# Gerar um UUID
uuid_128 = uuid.uuid4()

# Extrair os primeiros 64 bits (8 bytes) do UUID
uuid_64 = uuid_128.int >> 64

from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), default=uuid_64, nullable=False
    )
