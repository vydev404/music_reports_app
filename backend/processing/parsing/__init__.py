# -*- coding: utf-8 -*-
__all__ = ["EdlParser", "XmlParser", "ParserManager", "PARSERS"]
from .parsers import EdlParser, XmlParser
from .parser_manager import ParserManager

PARSERS = dict(edl=EdlParser, xml=XmlParser)
if __name__ == "__main__":
    print(f"Available parsers:{PARSERS.items()}")
