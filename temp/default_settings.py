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
from PySide6.QtCore import QRect
from PySide6.QtGui import QFont
from os import path

# MainWindow
GEOMETRY = QRect(0, 0, 1280, 720)
IS_MAXIMIZED = True
IS_CENTERED = True
FONT = QFont("Liberation Sans", 12, 400, False)
DATA_FILENAME = None
