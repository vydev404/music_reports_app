# -*- coding: utf-8 -*-
from dataclasses import asdict, dataclass
from pathlib import Path

from wavinfo import WavInfoReader


@dataclass
class MusicData:
    name: str
    artist: str
    title: str
    album: str
    right_holder: str
    path: str
    is_alive: bool = True

    @staticmethod
    def get_from_query(result) -> "MusicData":
        """
        Utility function to get data from a query result
            :param result:
            :return:
        """
        name, artist, track_name, album, right_holder, path, is_alive = result
        return MusicData(
            name=name,
            artist=artist,
            title=track_name,
            album=album,
            right_holder=right_holder,
            path=path,
            is_alive=is_alive,
        )

    def to_dict(self) -> dict[str, any]:
        return asdict(self)


class AudioMetadata:
    """
    Utility class for extracting metadata from audio files.
    """

    def get_music_data(self, file_path: str) -> MusicData:
        """
        Extracts music metadata from an audio file.

        :param file_path: Path to the audio file.
        :return: A MusicData object containing extracted metadata.
        """
        file_path = Path(file_path)
        audio_metadata = self.extract_wav_audio_info(file_path)
        return MusicData(
            name=file_path.name.upper(),
            artist=audio_metadata["artist"],
            title=audio_metadata["title"],
            album=audio_metadata["album"],
            right_holder=audio_metadata["technician"],
            path=str(file_path),
            is_alive=True,
        )

    @staticmethod
    def extract_wav_audio_info(file: Path) -> dict:
        """
        Extracts metadata from a WAV file.

        :param file: Path to the WAV file.
        :return: Dictionary containing metadata.
        """
        info = WavInfoReader(file)
        return info.info.to_dict()

    @staticmethod
    def extract_mp4_audio_info(file: Path):
        """
        Extracts metadata from an MP4 file.

        :param file: Path to the MP4 file.
        """
        raise NotImplemented
