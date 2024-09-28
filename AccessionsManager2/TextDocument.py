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
import html
from typing import Any
from PySide6.QtGui import (
    QTextDocument,
    QTextOption,
    QFont,
    QTextTable,
    QTextCursor,
    QTextTableFormat,
    QTextTableCellFormat,
)
from PySide6.QtCore import QSize, Qt
from DataTable import DataTable, DataTableModel
from text_edit import TextEdit


class TextDocument(QTextDocument):
    def __init__(self, content: Any):
        super().__init__()
        self.data_table: DataTable
        self.html: str
        if isinstance(content, DataTable):
            self.data_table = content
            self.create_from_data_table()

        self.setPageSize(QSize(792, 612))
        self.setDocumentMargin(36)
        self.setDefaultFont(QFont("Liberation Sans", 12, 400, False))

        text_edit = TextEdit(self)
        text_edit.exec()
        text_edit.close()

    def create_from_data_table(self):
        dt = self.data_table
        cursor = QTextCursor(self)

        table_format = QTextTableFormat()
        table_format.setCellSpacing(0)
        # table_format.setCellPadding(5)
        table_format.setBorder(0)
        # table_format.setBorderBrush(Qt.GlobalColor.black)

        table_cell_format = QTextTableCellFormat()
        # table_cell_format.setPadding(5)
        table_cell_format.setBottomBorder(1)
        # table_cell_format.setBorderBrush(Qt.GlobalColor.black)

        # table_format = table_cell_format.toTableFormat()
        # print(table_cell_format.bottomPadding())
        # print(table_cell_format.bottomBorder())
        # print(table_cell_format.bottomBorderBrush())

        model = self.data_table.model
        table = cursor.insertTable(model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)

        # for value in dt.column_headers:
        #     cell = text_table.cellAt(cursor)
        #     print(cursor.selectedTableCells())
        #     cursor.insertText(value)
        #     cursor.movePosition(QTextCursor.NextCell)
        # cursor.movePosition(
        #     QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.KeepAnchor
        # )
        # # cell.setFormat(table_cell_format)
        # cursor.setCharFormat(
        #     table_cell_format
        # )  # .mergeBlockCharFormat(table_cell_format)
        # cursor.movePosition(
        #     QTextCursor.MoveOperation.NextRow, QTextCursor.MoveMode.MoveAnchor
        # )
        # for row in dt.get_rows():
        #     for value in row:
        #         cell = text_table.cellAt(cursor)
        #         # cell.setFormat(table_cell_format)
        #         cursor.insertText(value)
        #         cursor.movePosition(QTextCursor.NextCell)

        # cursor.movePosition(QTextCursor.MoveOperation.NextCell)
        # text_table.resize(dt.num_rows, dt.num_cols)

    def html_func(self):
        dt = self.data_table
        html_str = """
<style>
    h1 {
        font-size: x-large;
    }

    th {
        border: 1px solid #000;
        margin: 0;
    }

    .row {
        border: 1px solid #000;
    }
</style>"""
        html_str += f"""
<h1>{dt.title}</h1>
<table>
    <thead>
        <tr id=headerRow>"""
        for header in dt.column_headers:
            html_str += f"""
            <th>{header.title()}</th>"""
        html_str += f"""
        </tr>
    </thead>
    <tbody>"""
        for row in dt.get_rows():
            html_str += f"""
        <tr class="row">"""
            for col in row:
                html_str += f"""
            <td>{col}</td>"""
            html_str += f"""
        </tr>"""
        html_str += """
    </tbody>
</table>"""
        return html_str
