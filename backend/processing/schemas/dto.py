# -*- coding: utf-8 -*-
from dataclasses import dataclass, field

from core.models import Music


@dataclass
class ClipDTO:
    clip_name: str
    source_in: int
    source_out: int
    tc_in: int
    tc_out: int
    clip_source_file: str

@dataclass
class FilteredClipDTO(ClipDTO):
    count: int
    duration_in_frames: int
    in_db: bool = False
    file_info: "MusicDTO" = None
    duration_in_tc: str = field(default="00:00:00")

    @staticmethod
    def get_from_clip(clip_data: ClipDTO, count: int = 0) -> "FilteredClipDTO":
        duration = clip_data.tc_out - clip_data.tc_in
        return FilteredClipDTO(
            clip_name=clip_data.clip_name,
            source_in=clip_data.source_in,
            source_out=clip_data.source_out,
            tc_in=clip_data.tc_in,
            tc_out=clip_data.tc_out,
            clip_source_file=clip_data.clip_source_file,
            count=count,
            duration_in_frames=duration,
        )


@dataclass
class ParsedDTO:
    duration: int = 0
    fps: int = 0
    data: list["ClipDTO"] = field(default_factory=list)
    timecode: str = field(default="00:00:00")


@dataclass
class FilteredDTO(ParsedDTO):
    data: dict[str, list[FilteredClipDTO] | list[ClipDTO]] = field(
        default_factory=dict
    )

    @staticmethod
    def get_from_parsed_data(parsed_data: "ParsedDTO"):
        f_data = dict(
            original_data=parsed_data.data, clips_in_db=[], clips_not_in_db=[]
        )
        return FilteredDTO(
            duration=parsed_data.duration,
            fps=parsed_data.fps,
            data=f_data,
            timecode=parsed_data.timecode,
        )

@dataclass
class MusicDTO:
    id: int
    name: str
    title: str
    right_holder: str
    album: str | None = None
    artist: str | None = None
    @staticmethod
    def get_from_query(result: Music) -> 'MusicDTO':
        return MusicDTO(
            id=result.id,
            name=result.name,
            artist=result.artist,
            title=result.title,
            album=result.album,
            right_holder=result.right_holder,
        )