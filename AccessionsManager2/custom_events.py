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
from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QApplication, QTableView


class DataFilenameChanged(QEvent):
    Type_ = QEvent.Type(QEvent.registerEventType())

    def __init__(self, filename: str):
        super().__init__(self.Type_)
        self.filename = filename


class FileSelectedEvent(QEvent):
    Type_ = QEvent.Type(QEvent.registerEventType())

    def __init__(self, filename: str):
        super().__init__(self.Type_)
        self.filename = filename


class SaveAllEvent(QEvent):
    Type_ = QEvent.Type(QEvent.registerEventType())

    def __init__(self):
        super().__init__(self.Type_)


class PrintTableEvent(QEvent):
    Type_ = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data_table: QTableView):
        super().__init__(self.Type_)
        self.data_table = data_table


# Custom event filter
def filter(receiver: QObject, event: QEvent):
    app = QApplication.instance()
    if event.type() == FileSelectedEvent.Type_:
        filename = event.filename
        app.load_file(filename)
    if event.type() == SaveAllEvent.Type_:
        app.save_settings()
    if event.type() == DataFilenameChanged.Type_:
        app.settings["data_filename"] = app.settings["data_filename"]._replace(
            value=event.filename
        )
    if event.type() == PrintTableEvent.Type_:
        app.print_data_table(event.data_table)
