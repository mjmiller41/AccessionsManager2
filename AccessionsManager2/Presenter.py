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
from typing import Text
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, QEvent
from View import View
from Model import Model
from DataTable import DataTable
from Settings import Settings
from TextDocument import TextDocument
import custom_events
import resources_rc


class Presenter(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.settings_obj = Settings()
        self.settings = self.settings_obj.settings
        self.model = Model(self.settings)
        self.view = View(self, self.settings, self.model.dataframes)

    # Override base's notify function, call base's notify after filtering
    def notify(self, receiver: QObject, event: QEvent):
        custom_events.filter(receiver, event)
        return super().notify(receiver, event)

    def save_settings(self):
        self.settings_obj.save_all()

    def load_file(self, filename: str):
        self.model.load_data_file(filename)
        self.view.create_tab_widget(self.model.dataframes)

    def print_data_table(self, data_table: DataTable):
        txt_doc = TextDocument(data_table)

    def settings_action_triggered(self, checked: bool): ...
