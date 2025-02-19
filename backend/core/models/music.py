from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Music(Base):
    __tablename__ = "music_library"

    name: Mapped[str] = mapped_column(String(255), nullable=False, )
    title: Mapped[str] =  mapped_column(String(64), nullable=False)
    artist: Mapped[str] = mapped_column(String(64), nullable=True)
    album: Mapped[str] = mapped_column(String(64), nullable=True)
    right_holder: Mapped[str] = mapped_column(String(64), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    is_alive: Mapped[bool]
