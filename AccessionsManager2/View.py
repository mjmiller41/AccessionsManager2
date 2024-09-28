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
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QToolBar,
    QMenu,
    QFileDialog,
    QDialog,
)
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen, QIcon, QAction, QCloseEvent, QPainter
from PySide6.QtTest import QTest
from pandas import DataFrame
from typing import Sequence, Protocol
from DataTable import DataTable
from Settings import Settings, AttrNTup
import helpers
from custom_events import FileSelectedEvent, SaveAllEvent, PrintTableEvent
import resources_rc


class Presenter(Protocol):
    def save_all(): ...


class View(QMainWindow):
    def __init__(
        self,
        presenter: Presenter,
        settings: Settings,
        dataframes: Sequence[DataFrame] | None = None,
    ):
        super().__init__()
        self.settings: dict[str, AttrNTup] = settings
        self.tab_widget: QTabWidget

        self.init_main_window()
        self.create_menu(presenter)
        self.create_toolbar(presenter)
        self.create_tab_widget(dataframes)

        # For print testing only
        data_table = self.tab_widget.currentWidget()
        QApplication.postEvent(self, PrintTableEvent(data_table))
        # self.close()

    def create_menu(self, presenter: Presenter):
        self.menu_bar = self.menuBar()
        self.file_menu = QMenu("&File", self)
        self.menu_bar.addMenu(self.file_menu)

        self.open_file_action = self.file_menu.addAction(
            QIcon(":/icons/folder-open.png"), "&Open file"
        )
        self.file_menu.addAction(self.open_file_action)
        self.open_file_action.triggered.connect(self.open_file)

        self.save_file_action = self.file_menu.addAction(
            QIcon(":/icons/disk.png"), "&Save file"
        )
        self.file_menu.addAction(self.save_file_action)
        self.save_file_action.triggered.connect(self.save_file)

        self.print_action = self.file_menu.addAction(
            QIcon(":/icons/printer.png"), "&Print"
        )
        self.file_menu.addAction(self.print_action)
        self.print_action.triggered.connect(self.print_)

        self.settings_action = self.file_menu.addAction(
            QIcon(":/icons/gear.png"), "&Settings"
        )
        self.file_menu.addAction(self.settings_action)
        self.settings_action.triggered.connect(self.open_settings)

        self.exit_action = self.file_menu.addAction(QIcon(":/icons/cross.png"), "E&xit")
        self.file_menu.addAction(self.exit_action)
        self.exit_action.triggered.connect(self.close)

    def create_toolbar(self, presenter: Presenter):
        self.toolbar = QToolBar("Toolbar", self)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addToolBar(self.toolbar)

        self.load_file_action = QAction(
            QIcon(":/icons/folder-open.png"), "Open File", self
        )
        self.load_file_action.setStatusTip("Load a new spreadsheet file")
        self.load_file_action.triggered.connect(self.open_file)
        self.toolbar.addAction(self.load_file_action)

        self.print_view_action = QAction(
            QIcon(":/icons/printer.png"), "Print View", self
        )
        self.print_view_action.setStatusTip("Print the records in the current view")
        self.print_view_action.triggered.connect(self.print_)
        self.toolbar.addAction(self.print_view_action)

    def create_tab_widget(self, dataframes: Sequence[DataFrame] | None):
        if dataframes is not None:
            self.tab_widget = QTabWidget(self)
            self.setCentralWidget(self.tab_widget)
            helpers.set_font_bold(self.tab_widget.tabBar())
            for dataframe in dataframes:
                data_table = DataTable(dataframe)
                self.tab_widget.addTab(data_table, dataframe.name)

    def center_window(self):
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def init_main_window(self):
        self.setWindowTitle("Accessions Manager 2")
        self.setWindowIcon(QIcon(":/icons/logo.ico"))
        self.setGeometry(self.settings["geometry"].value)
        self.setFont(self.settings["font"].value)
        if self.settings["is_maximized"].value:
            self.showMaximized()
        else:
            self.show()
            self.center_window()

    def open_file(self, _):
        file_dialog = QFileDialog(self)
        filename, _ = file_dialog.getOpenFileName(
            self, "Open Spreadsheet", "./", "Open Document Spreadsheet(*.ods)"
        )
        QApplication.postEvent(self, FileSelectedEvent(filename))

    def save_file(self): ...
    def open_settings(self): ...
    def print_(self):
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec() == QDialog.Accepted:
            data_table = self.tab_widget.currentWidget()
            QApplication.postEvent(self, PrintTableEvent(data_table))
            # painter = QPainter(printer)
            # self.tab_widget.currentWidget().render(painter)
            # painter.end()

    # Override of QApplication closeEvent
    def closeEvent(self, event: QCloseEvent):
        print("Main Window Closing...")
        QApplication.postEvent(self, SaveAllEvent())
        super().closeEvent(event)
