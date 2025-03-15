# -*- coding: utf-8 -*-


class TimecodeConverter:
    @staticmethod
    def timecode_to_frames(timecode: str, fps: int = 25) -> int:
        """
        Converts a timecode string to a frame count.
        :param timecode: The timecode string in the format HH:MM:SS:FF.
        :param fps: Frames per second. Default is 25.
        :return: The total frame count.
        :raises ParsingError: If the timecode format is invalid.
        """

        try:
            parts = timecode.split(":")
            if len(parts) != 4:
                raise ValueError(
                    f"Invalid timecode format: '{timecode}'. Expected format: HH:MM:SS:FF"
                )
            hours, minutes, seconds, frames = map(int, parts)
            if not (0 <= minutes < 60 and 0 <= seconds < 60 and 0 <= frames < fps):
                raise ValueError(
                    f"Invalid timecode values: '{timecode}'. Check MM, SS, FF ranges."
                )
            frame_count = ((hours * 60 + minutes) * 60 + seconds) * fps + frames
            return frame_count

        except ValueError as e:
            raise ValueError(f"Failed to parse timecode '{timecode}': {e}")

    @staticmethod
    def frames_to_timecode(frames: int, fps: int = 25) -> str:
        """
        Converts a frame count to a timecode string.

        :param frames: The total frame count.
        :param fps: Frames per second. Default is 25.
        :return: The timecode string in the format HH:MM:SS.
        """
        try:
            if not isinstance(frames, int):
                raise TypeError(
                    f"Invalid frames type must be int, received - {type(frames)} "
                )
            seconds, frames = divmod(frames, fps)
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            seconds = seconds + 1 if frames > fps // 2 else seconds
            return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
        except Exception as e:
            raise ValueError(f"Failed convert frames timecode: {e}")


if __name__ == "__main__":
    tc = TimecodeConverter.timecode_to_frames("25:62:01:20")
    print(tc)
