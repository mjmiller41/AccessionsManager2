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
from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QTableView
from PySide6.QtGui import QFontMetrics, QFont
from pandas import DataFrame
from typing import Sequence
import helpers


class DataTableModel(QAbstractTableModel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])


class DataTable(QTableView):
    def __init__(self, dataframe: DataFrame):
        super().__init__()
        self.dataframe: DataFrame = dataframe
        self.title = self.dataframe.name.title()

        self.column_headers: Sequence[str] = self.dataframe.columns
        self.model = DataTableModel(self, self.dataframe)
        self.setModel(self.model)
        self.num_rows = self.model.rowCount(0)
        self.num_cols = self.model.columnCount(0)

        self.setAlternatingRowColors(True)
        helpers.set_font_bold(self.horizontalHeader())
        self.set_column_widths()

    def get_rows(self) -> Sequence[Sequence[str]]:
        rows = []
        for row in range(self.num_rows):
            row_values = []
            for col in range(self.num_cols):
                index = self.model.index(row, col)
                value = self.model.data(index, Qt.DisplayRole)
                row_values.append(value)
            rows.append(row_values)
        return rows

    def set_column_widths(self):
        flag: int = Qt.TextFlag.TextSingleLine.value
        font = QFont("Liberation Sans")
        font_metrics = QFontMetrics(font)
        # Iterate through columns and set column width
        for i, header in enumerate(self.column_headers):
            min_width = font_metrics.size(flag, str(header)).width()
            column_items = self.dataframe[header].array
            for item in column_items:
                # Find the width in pixels of the item as a string
                text_width = font_metrics.size(flag, str(item)).width()
                if text_width > min_width:
                    min_width = text_width
            self.setColumnWidth(i, min_width + 10)
