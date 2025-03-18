class ParserManager:
    """
    Manages the registration and retrieval of file parsers based on file type.
    """

    def __init__(self):
        self.parsers = {}

    def register_parser(self, file_type: str, parser: "BaseParser"):
        """
        Registers a parsing for a specific file type.

        :param file_type: The type of file the parsing handles.
        :param parser: The parsing instance to register.
        """
        self.parsers[file_type] = parser

    def get_parser(self, file_type: str):
        """
        Retrieves the parsing for a specific file type.

        :param file_type: The type of file to parse.
        :return: The parsing instance or None if not found.
        """
        if file_type in self.parsers:
            return self.parsers[file_type]
        else:
            raise KeyError(
                f"Parser manager cannot find parsing for file type '{file_type}'"
            )
