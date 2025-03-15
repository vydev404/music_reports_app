# -*- coding: utf-8 -*
import re
from abc import ABC
from pathlib import Path
from xml.etree import ElementTree

from proccessing.parser.dto import ParsedData, ClipData
from utils.timecode_converter import TimecodeConverter as tc


class ParserManager:
    """
    Manages the registration and retrieval of file parsers based on file type.
    """

    def __init__(self):
        self.parsers = {}

    def register_parser(self, file_type: str, parser: "BaseParser"):
        """
        Registers a parser for a specific file type.

        :param file_type: The type of file the parser handles.
        :param parser: The parser instance to register.
        """
        self.parsers[file_type] = parser

    def get_parser(self, file_type: str):
        """
        Retrieves the parser for a specific file type.

        :param file_type: The type of file to parse.
        :return: The parser instance or None if not found.
        """
        if file_type in self.parsers:
            return self.parsers[file_type]
        else:
            raise KeyError(
                f"Parser manager cannot find parser for file type '{file_type}'"
            )


class BaseParser(ABC):
    def parse(self, file_path: str):
        raise NotImplementedError


class EdlParser(BaseParser):
    """
    Parses EDL files and converts them into ParsedData format.
    """

    def parse(self, file_path: Path) -> ParsedData:
        """
        Parses an EDL file and extracts relevant data into ParsedData.

        :param file_path: Path to the EDL file.
        :return: ParsedData instance containing parsed file data.
        :raises ParsingError: If an error occurs during parsing.
        """
        parsed_data = ParsedData()
        cached_line = None
        try:
            with open(file_path, "r") as file:
                original_lines = file.readlines()
                if not len(original_lines):
                    raise ValueError(f"No data found in '{file_path}'")
                start_tc, end_tc = None, None
                for line in original_lines:
                    line = line.strip()
                    if cached_line is None:
                        cached_line = line
                        continue
                    if line.startswith("*"):
                        cached_line += line[1:].strip()
                        continue
                    clip_data = self.parse_edl_line(cached_line)
                    if not clip_data:
                        cached_line = line
                        continue
                    start_tc = start_tc or clip_data.tc_in
                    end_tc = max(end_tc or 0, clip_data.tc_out)
                    # Remove duplicates
                    if clip_data in parsed_data.data:
                        cached_line = line
                        continue
                    parsed_data.data.append(clip_data)
                    cached_line = line

                if start_tc is not None and end_tc is not None:
                    parsed_data.duration = end_tc - start_tc
                    parsed_data.timecode = tc.frames_to_timecode(
                        parsed_data.duration, parsed_data.fps
                    )

        except FileNotFoundError as e:
            raise e
        except IOError as e:
            raise e
        except Exception as e:
            raise e
        return parsed_data

    @staticmethod
    def parse_edl_line(line: str) -> bool | ClipData:
        """
        Parses a single EDL file line and converts it into ClipData.

        :param line: A line from the EDL file.
        :return: ClipData instance or False if the line is invalid.
        """
        clean_pattern = r"((?:\d{2}:\d{2}:\d{2}:\d{2}\s*){4})([\w\d_, ]+:?)"
        line = re.sub(clean_pattern, r"\1", line)
        parts = re.split(r"\s+", line)

        if len(parts) < 8:
            return False
        try:
            formatted_data = ClipData(
                clip_name=parts[1],
                source_in=tc.timecode_to_frames(parts[4]),
                source_out=tc.timecode_to_frames(parts[5]),
                tc_in=tc.timecode_to_frames(parts[6]),
                tc_out=tc.timecode_to_frames(parts[7]),
                clip_source_file="".join(parts[8:]).upper(),
            )

            return formatted_data
        except Exception as e:
            return False


# XmlParser
class XmlParser(BaseParser):
    def parse(self, file_path: Path) -> ParsedData:
        """
        Parses an XML file and returns ParsedData.

        :param file_path: Path to the XML file.
        :return: ParsedData object containing parsed clips information.
        """
        parsed_data = ParsedData()
        sequence = None
        try:
            tree = ElementTree.parse(file_path)
            root = tree.getroot()
            if root[0].tag == "sequence":
                sequence = root[0]
        except Exception as e:
            raise e

        try:
            media_tag = None
            for tag in sequence:
                value = tag.tag
                if value == "duration":
                    parsed_data.duration = int(tag.text)
                elif value == "rate":
                    parsed_data.fps = int(tag.find("timebase").text)
                elif value == "media":
                    media_tag = tag

            parsed_data.timecode = tc.frames_to_timecode(
                parsed_data.duration, parsed_data.fps
            )
            audio_tracks = media_tag.find("audio").findall("track")
            track_id = 1
            file_ids = []

            for track in audio_tracks:
                if len(track) <= 1:
                    continue
                for clip in track.findall("clipitem"):
                    file_id = clip.find("file").attrib["id"]
                    clip_name = ""

                    if clip.find("file").findall("name"):
                        clip_name = clip.find("file").find("name").text
                        file_ids.append({"file_id": file_id, "clip_name": clip_name})
                    else:
                        for item in file_ids:
                            if file_id == item.get("file_id"):
                                clip_name = item.get("clip_name")
                    tc_in = int(clip.find("in").text)
                    tc_out = int(clip.find("out").text)
                    source_in = int(clip.find("start").text)
                    source_out = int(clip.find("end").text)

                    clip_data = ClipData(
                        clip_name=clip_name,
                        tc_in=tc_in,
                        tc_out=tc_out,
                        source_in=source_in,
                        source_out=source_out,
                        clip_source_file=clip_name.upper(),
                    )

                    if clip_data in parsed_data.data:
                        continue

                    parsed_data.data.append(clip_data)
                track_id += 1
            return parsed_data

        except Exception as e:
            raise e
