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
from collections import namedtuple
from PySide6.QtCore import QSettings
from typing import Any
from PySide6.QtCore import QRect
from PySide6.QtGui import QFont
from enum import Enum
import resources_rc

# Default values
ORGANIZATION_NAME = "MJMSoft"
APPLICATION_NAME = "Accessions Manager 2"
FORMAT = QSettings.Format.NativeFormat


class GROUP(Enum):
    VIEW = "View"
    MODEL = "Model"
    PRESENTER = "Presenter"


# Named tupple used to store settings defaults
AttrNTup = namedtuple("attr", ["value", "group", "key", "type"])
# Setting defaults
GEOMETRY = AttrNTup(QRect(0, 0, 1280, 720), GROUP.VIEW, "geometry", QRect)
IS_MAXIMIZED = AttrNTup(False, GROUP.VIEW, "is_maximized", bool)
FONT = AttrNTup(QFont("Liberation Sans", 12, 400, False), GROUP.VIEW, "font", QFont)
DATA_FILENAME = AttrNTup("", GROUP.MODEL, "data_filename", str)


class Settings(QSettings):

    def __init__(self):
        super().__init__(ORGANIZATION_NAME, APPLICATION_NAME)
        self.settings: dict[str, AttrNTup] = {
            "geometry": GEOMETRY,
            "is_maximized": IS_MAXIMIZED,
            "font": FONT,
            "data_filename": DATA_FILENAME,
        }
        self.init_settings()
        if self.defaultFormat() != FORMAT:
            self.setDefaultFormat(FORMAT)

    def read_setting(self, group: GROUP, key: str, type: object):
        self.beginGroup(group.value)
        value = self.value(key, type=type)
        self.endGroup()
        return value

    def write_setting(self, group: GROUP, key: str, value: Any):
        self.beginGroup(group.value)
        self.setValue(key, value)
        self.endGroup()

    def init_settings(self):
        for key, setting in self.settings.items():
            self.settings[key] = setting._replace(
                value=self.read_setting(setting.group, setting.key, setting.type)
            )

    def save_all(self):
        for setting in self.settings.values():
            self.write_setting(setting.group, setting.key, setting.value)

    def save(self, setting: AttrNTup):
        self.write_setting(setting.group, setting.key, setting.value)
