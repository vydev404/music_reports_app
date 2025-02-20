import datetime
import uuid
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

#custom fields
uuid_pk = Annotated[UUID, mapped_column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)]
created_at_field = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at_field = Annotated[datetime.datetime, mapped_column(
     server_default=text("TIMEZONE('utc', now())"),
     onupdate=datetime.datetime.now
)]
class Base(DeclarativeBase):
    __abstract__ = True
    id = Mapped[uuid_pk]
    created_at = Mapped[created_at_field]
    updated_at = Mapped[updated_at_field]
