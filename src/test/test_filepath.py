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
import unittest
from pathlib import Path

from src.promptbouncer.util.file_path_util import FilePathUtil

SRC_ROOT = "promptbouncer"


class TestFilePath(unittest.TestCase):
    def test_app_root_path(self) -> None:
        path = Path(FilePathUtil.app_root_path())
        self.assertTrue(path.is_dir())
        self.assertTrue(SRC_ROOT in path.__str__())

    def test_api_spec_path(self) -> None:
        path = Path(FilePathUtil.api_spec_path())
        print(path)
        self.assertTrue(path.is_file())


if __name__ == "__main__":
    unittest.main()
