#  Copyright (c) 2024 seamus@corvideon.ie
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import os
from pathlib import Path

from src.promptbouncer.config.api import OPEN_API_YAML_SPEC_FILE


class FilePathUtil:
    """For handling file paths in the app."""

    def __init__(self):
        """Not needed in static utility class."""
        pass

    @staticmethod
    def app_root_path() -> str:
        script_path: Path = Path(__file__)
        return script_path.parent.parent.absolute().__str__()

    @staticmethod
    def repo_root_path() -> str:
        script_path: Path = Path(__file__)
        return script_path.parent.parent.parent.parent.absolute().__str__()

    @staticmethod
    def api_spec_path() -> str:
        return FilePathUtil.append_path_to_app_path(OPEN_API_YAML_SPEC_FILE)

    @staticmethod
    def append_path_to_app_path(path_str: str) -> str:
        app_root: str = FilePathUtil.app_root_path()
        return os.path.join(app_root, path_str)

    @staticmethod
    def append_path_to_repo_path(path_str: str) -> str:
        app_root: str = FilePathUtil.repo_root_path()
        return os.path.join(app_root, path_str)
