# -*- coding: utf-8 -*-
import hashlib
import re
import time
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class FileMetadata:
    path: str
    full_name: str
    name: str
    type: str

    def to_dict(self) -> dict[str, any]:
        return asdict(self)


class FileUtils:
    """
    Utility class for handling file validation, metadata extraction, and hash calculation.
    """

    # full_pattern = re.compile(r"^[A-Za-z]+_\d{6}_[A-Za-z0-9_]+$")
    # Patterns for file name validation
    # full_pattern = re.compile(r"(^[A-Za-z0-9_]*)(\d{6})_([A-Za-z0-9_]+$)")
    # type_pattern = re.compile(r"^[A-Za-z]+$")
    # date_pattern = re.compile(r"^\d{6}$")
    # name_pattern = re.compile(r"^[A-Za-z0-9_]+$")

    @staticmethod
    def get_file_metadata(file_path: Path) -> FileMetadata:
        """
        Extracts metadata from a file, validates it, and returns a `FileData` object.
        :param file_path: Path to the file.
        :return: FileData object containing validated file information.
        :raises ValidationError: If the file does not exist, has an invalid name, or an unsupported type.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist.")
        try:
            file_name = file_path.stem
            file_type = file_path.suffix.strip(".")
            full_name = file_path.name

            return FileMetadata(
                path=str(file_path),
                full_name=full_name,
                name=file_name,
                type=file_type,
            )
        except Exception as e:
            raise e

    @staticmethod
    def validate_name(file_name: str) -> None:
        """
        Validates the file name against predefined patterns.

        :param file_name: The name of the file to validate.
        :raises ValidationError: If the file name format is incorrect.
        """
        full_pattern = re.compile(r"(^[A-Za-z0-9_]*)(\d{6})_([A-Za-z0-9_]+$)")
        match = full_pattern.match(file_name)
        if match is None:
            raise ValueError(
                f"Filename '{file_name}' does not match the expected pattern."
            )

    @staticmethod
    def validate_file_type(file_type: Path) -> None:
        """
        Validates the file type against supported types.

        :param file_type: The file type extension.
        :raises ValidationError: If the file type is unsupported.
        """
        # type_pattern = re.compile(r"^[A-Za-z]+$")
        pass

    @staticmethod
    def calculate_file_hash(file_path: Path) -> str:
        """
        Computes the MD5 hash of a file.

        :param file_path: Path to the file.
        :return: MD5 hash as a hexadecimal string.
        :raises ValidationError: If the file cannot be read.
        """
        try:
            hasher = hashlib.md5()
            with file_path.open("rb") as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (FileNotFoundError, PermissionError) as e:
            raise e

    @staticmethod
    def is_file_fully_copied(file_path: Path, retries=5, delay=5) -> bool:
        """
        Checks if a file has been fully copied by comparing its size over time.
        :param file_path: Path to the file.
        :param retries: Number of checks before assuming the file is still being copied.
        :param delay: Time in seconds between checks.
        :return: True if the file is fully copied, False otherwise.
        """
        previous_size = -1
        for _ in range(retries):
            try:
                current_size = file_path.stat().st_size
                if current_size == previous_size:
                    return True  # File size is stable, meaning it's fully copied

                previous_size = current_size
                time.sleep(delay)
            except (FileNotFoundError, PermissionError) as e:
                time.sleep(delay)
        return False  # If size kept changing, file is still copying
