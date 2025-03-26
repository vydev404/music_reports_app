# -*- coding: utf-8 -*-
import enum
from dataclasses import dataclass, field, asdict


class TaskStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskProcessingStage(str, enum.Enum):
    VALIDATING = "VALIDATING"
    PARSING = "PARSING"
    FILTERING = "FILTERING"
    REPORTING = "REPORTING"
    MOVING = "MOVING"


# Base Data Objects
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
    clip_info: "MusicDTO" = None
    duration: dict[str, int | str] = field(default_factory=dict)

    @staticmethod
    def get_from_clip(clip_data: ClipDTO, count: int = 0) -> "FilteredClipDTO":
        duration_in_frames = clip_data.tc_out - clip_data.tc_in
        duration = dict(frames=duration_in_frames, timecode="00:00:00")
        return FilteredClipDTO(
            clip_name=clip_data.clip_name,
            source_in=clip_data.source_in,
            source_out=clip_data.source_out,
            tc_in=clip_data.tc_in,
            tc_out=clip_data.tc_out,
            clip_source_file=clip_data.clip_source_file,
            count=count,
            duration=duration,
        )


@dataclass
class ParsedDTO:
    fps: int = 0
    items: list["ClipDTO"] = field(default_factory=list)
    total_duration: dict[str, int | str] = field(default_factory=dict)


@dataclass
class FilteredDTO(ParsedDTO):
    items: dict[str, list[FilteredClipDTO] | None] = field(default_factory=dict)

    @staticmethod
    def get_from_parsed_data(parsed_data: "ParsedDTO"):
        extended_items = dict(items_in_db=None, items_not_in_db=None)
        return FilteredDTO(
            total_duration=parsed_data.total_duration,
            fps=parsed_data.fps,
            items=extended_items,
        )


@dataclass
class MusicDTO:
    id: int
    name: str
    title: str
    right_holder: str
    album: str | None = None
    artist: str | None = None

    # @staticmethod
    # def get_from_query(result: Music) -> "MusicDTO":
    #     return MusicDTO(
    #         id=result.id,
    #         name=result.name,
    #         artist=result.artist,
    #         title=result.title,
    #         album=result.album,
    #         right_holder=result.right_holder,
    #     )

    @staticmethod
    def from_response(response: dict) -> "MusicDTO":
        return MusicDTO(
            id=response["id"],
            name=response["name"],
            title=response["title"],
            artist=response["title"],
            album=response["album"],
            right_holder=response["right_holder"],
        )


@dataclass
class UsedMusicDTO:
    id: int
    title: str
    count: int
    duration: str

    def to_dict(self) -> dict[str, int | str]:
        return asdict(self)


@dataclass
class SourceFileDTO:
    id: int
    name: str
    path: str
    type: str
    created: str = None
    data: FilteredDTO | None = None

    # @staticmethod
    # def get_from_query(result: SourceFile) -> "SourceFileDTO":
    #     return SourceFileDTO(
    #         id=result.id,
    #         name=result.name,
    #         path=result.path,
    #         type=result.type,
    #     )

    @staticmethod
    def from_response(response: dict) -> "SourceFileDTO":
        return SourceFileDTO(
            id=response["id"],
            name=response["name"],
            path=response["path"],
            type=response["type"].strip("."),
        )


@dataclass
class TaskDTO:
    source_file_id: int
    id: int
    status: str
    error_stage: str | None
    error_message: str | None
    created_at: str
    updated_at: str

    def to_dict(self) -> dict[str, int | str]:
        return asdict(self)

    @staticmethod
    def from_response(response: dict) -> "TaskDTO":
        return TaskDTO(
            source_file_id=response["source_file_id"],
            id=response["id"],
            status=response["status"],
            error_stage=response["error_stage"],
            error_message=response["error_message"],
            created_at=response["created_at"],
            updated_at=response["updated_at"],
        )


@dataclass
class ReportDTO:
    name: str
    file: str
    source_file_id: int
    used_music: list[dict | None] = field(default_factory=list)

    def to_dict(self) -> dict[str, int | str]:
        return asdict(self)

    # used music format [
    #     {
    #         "id": 1,
    #         "count": 2,
    #         "duration": "00:02:15",
    #         "title": "Song A"
    #     },
    #     {
    #         "id": 3,
    #         "count": 1,
    #         "duration": "00:01:30",
    #         "title": "Song B"
    #     }
    # ]
