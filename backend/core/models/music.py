from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Music(Base):
    __tablename__ = "music_library"

    name: Mapped[str] = mapped_column()
    title: Mapped[str]
    artist: Mapped[str]
    album: Mapped[str]
    right_holder: Mapped[str]
    path: Mapped[str]
    is_alive: Mapped[bool]
