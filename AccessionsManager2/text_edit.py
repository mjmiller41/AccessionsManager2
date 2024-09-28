# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PySide6.QtCore import QCoreApplication, QObject, QRect
from PySide6.QtWidgets import QMainWindow, QTextEdit, QDialog, QVBoxLayout, QDockWidget
from PySide6.QtGui import QTextDocument


class TextEdit(QDialog):
    def __init__(self, document: QTextDocument):
        super().__init__()
        self.setWindowTitle(QCoreApplication.applicationName())
        self.setGeometry(QRect(300, 200, 1280, 720))

        text_edit = QTextEdit(self)
        text_edit.setDocument(document)

        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        self.setLayout(layout)
