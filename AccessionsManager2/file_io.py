#!.venv/Scripts/python
# coding=utf-8
"""
Copyright 2024, Michael Joseph Miller #

This file is part of AccessionsManager2.

AccessionsManager2 is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

AccessionsManager2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License
along with AccessionsManager2. If not,
see <https: //www.gnu.org/licenses/>.
"""
from __future__ import annotations
from pandas import ExcelFile, DataFrame
from pandas.io.excel._base import ExcelFile
from odf.opendocument import OpenDocument
from datetime import datetime
from time import sleep
import tempfile
import os
from typing import Sequence
from helpers import validate_file_data


def load_document(data_location: str) -> Sequence[DataFrame] | None:
    path = os.path.abspath(data_location)
    with ExcelFile(path, engine="odf") as xls:
        file_data = xls.parse(
            sheet_name=None,
            keep_default_na=False,
        )  # type: ignore
    xls.close()
    dataframes = validate_file_data(file_data)
    return dataframes


# def print_doc(doc: OpenDocument):
#     # Create temp file
#     filename = tempfile.mktemp(".odt")
#     default_printer = win32print.GetDefaultPrinter()

#     # Write doc to file
#     with open(filename, "wb") as f:
#         doc.write(f)
#         f.close()
#     # Print from shell
#     x_code = win32api.ShellExecute(
#         0,
#         "print",
#         filename,
#         '/d:"%s"' % default_printer,
#         ".",
#         0,
#     )
#     sleep(5)
#     file_deleted = False
#     while not file_deleted:
#         try:
#             os.remove(filename)
#             file_deleted = True
#             print("Temp file deleted")
#         except PermissionError:
