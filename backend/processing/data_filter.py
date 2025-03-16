from core.repositories import MusicRepository
from processing.schemas.dto import FilteredDTO, FilteredClipDTO, ParsedDTO, MusicDTO
from utils.timecode_converter import TimecodeConverter as tc


class ParsedDataFilter:
    def __init__(self, repository: MusicRepository):
        self.repository = repository

    async def filter_parsed_data(self, parsed_data: ParsedDTO) -> FilteredDTO:
        """
        Filters parsed data: remove duplicates, count usage, sum usage duration,
         check and fetch music meta from db and return filtered data.
        :param parsed_data: ParsedDTO received after parsing
        :return: filtered data objects as FilteredDTO instance
        """
        filtered_data = FilteredDTO.get_from_parsed_data(parsed_data)
        unique_clips = {}
        original_data = parsed_data.data
        # remove duplicates by ClipData.source name, and sum all durations
        if not len(original_data):
            raise ValueError("Received empty data object")
        for clip in original_data:
            if clip.clip_source_file not in unique_clips:
                filtered_clip_data = FilteredClipDTO.get_from_clip(clip)
                filtered_clip_data.count = 1
                unique_clips[clip.clip_source_file] = filtered_clip_data
                continue
            clip_duration = clip.tc_out - clip.tc_in
            unique_clips[clip.clip_source_file].duration_in_frames+= clip_duration
            unique_clips[clip.clip_source_file].count+= 1
            unique_clips[clip.clip_source_file].duration_in_tc = tc.frames_to_timecode(unique_clips[clip.clip_source_file].duration_in_frames)

        # check if clip source file contains in music_library, end get additional info about file from db
        for clip in unique_clips:
            db_result = await self.repository.get_by_name(clip)
            if not db_result:
                filtered_data.data['clips_not_in_db'].append(unique_clips[clip])
            clip_data = unique_clips[clip]
            clip_data.in_db = True
            music_info = MusicDTO.get_from_query(db_result)
            clip_data.file_info = music_info
            filtered_data.data['clips_in_db'].append(clip_data)
        return filtered_data
