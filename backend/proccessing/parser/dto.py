# -*- coding: utf-8 -*-
from dataclasses import dataclass, field


@dataclass
class ClipData:
    clip_name: str
    source_in: int
    source_out: int
    tc_in: int
    tc_out: int
    clip_source_file: str


@dataclass
class FormatedClipData(ClipData):
    count: int
    duration_in_frames: int
    in_db: bool = False
    file_info: "MusicData" = None
    duration_in_tc: str = field(default="00:00:00")

    @staticmethod
    def get_from_clip_data(clip_data: ClipData, count: int = 0) -> "FormatedClipData":
        duration = clip_data.tc_out - clip_data.tc_in
        return FormatedClipData(
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
class ParsedData:
    duration: int = 0
    fps: int = 0
    data: list["ClipData"] = field(default_factory=list)
    timecode: str = field(default="00:00:00")


@dataclass
class FormatedData(ParsedData):
    data: dict[str, list[FormatedClipData] | list[ClipData]] = field(
        default_factory=dict
    )

    @staticmethod
    def get_from_parsed_data(parsed_data: "ParsedData"):
        f_data = dict(
            original_data=parsed_data.data, clips_in_db=[], clips_not_in_db=[]
        )
        return FormatedData(
            duration=parsed_data.duration,
            fps=parsed_data.fps,
            data=f_data,
            timecode=parsed_data.timecode,
        )
