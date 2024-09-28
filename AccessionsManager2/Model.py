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
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from pandas import DataFrame
from typing import Mapping, Sequence
from Settings import AttrNTup
import file_io
from custom_events import DataFilenameChanged
import resources_rc


class Model(QObject):
    def __init__(self, settings: Mapping[str, AttrNTup]):
        super().__init__()
        self._data_filename: str = settings["data_filename"].value
        self.dataframes: Sequence[DataFrame] | None = None
        self.load_data_file()

    @property
    def data_filename(self):
        return self._data_filename

    @data_filename.setter
    def data_filename(self, value):
        self._data_filename = value
        QApplication.postEvent(self, DataFilenameChanged(value))

    def load_data_file(self, filename: str | None = None):
        self.data_filename = filename if filename else self.data_filename
        if self.data_filename != "":
            dataframes = file_io.load_document(self.data_filename)
            if len(dataframes) > 0:
                self.dataframes = dataframes
            else:
                print(f"{self.data_filename} was not loaded successfully")
