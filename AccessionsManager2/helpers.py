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
from PySide6.QtWidgets import QWidget
from pandas import DataFrame
from pandas.io.excel._base import ExcelFile
from datetime import datetime
from typing import Sequence
import copy as cpy


def strip(x: str) -> str:
    if isinstance(x, str):
        x = x.strip()
    return x


def strf_mdy(x):
    if isinstance(x, datetime):
        x = x.strftime("%d/%m/%Y")
    return x


def columns(dataframe: DataFrame) -> Sequence[str]:
    cols = []
    for heading in dataframe.columns:
        cols.append(str(heading).title())
    return cols


def set_font_bold(item: QWidget):
    font = item.font()
    font.setBold(True)
    item.setFont(font)


def clean_loaded_data(dataframe: DataFrame) -> DataFrame:
    new_df = cpy.deepcopy(dataframe)
    new_df = new_df.map(strip)
    new_df = new_df.map(strf_mdy)
    new_df.columns = columns(dataframe)
    return new_df


def validate_file_data(file_data: ExcelFile) -> Sequence[DataFrame] | None:
    dataframes: list[DataFrame] = []
    if isinstance(file_data, DataFrame):
        dataframe = clean_loaded_data(file_data)
        dataframe.name = sheet_names[0].title()  # type: ignore
        dataframes.append(dataframe)
    else:
        for name, data_df in file_data.items():
            dataframe = clean_loaded_data((data_df))
            dataframe.name = name.title()
            dataframes.append(dataframe)
    return dataframes if len(dataframes) > 0 else None
