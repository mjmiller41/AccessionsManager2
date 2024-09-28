from PySide6.QtCore import Qt, QCoreApplication
import darkdetect as dt
from temp.colors import *

IS_DARK = dt.isDark()

QCoreApplication.setAttribute(Qt.AA_UseStyleSheetPropagationInWidgetStyles, True)


def stylesheet():
    return f"""
QMainWindow * {{
    font: normal 12pt 'Liberation Sans';
}}

QMenuBar {{
    background-color: {HILIGHT};
    border-top: 3px solid {HOTTRACKINGCOLOR};
    font: normal 10pt 'Liberation Sans';
    padding-left: 5px;
}}

QMenuBar::item {{
    padding-top: 10px;
    padding-bottom: 5px;
    padding-left: 10px;
    padding-right: 10px;
}}

QMenuBar::item:hover {{
    background-color: {WINDOW};
}}

QMenu {{
    font: normal 10pt 'Liberation Sans';
}}

QMenu::item {{
}}

QTabBar::tab {{
    top: 3px;
    margin: 0px 1px;
    padding: 2px;
    background-color: {HILIGHT};
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    border-left: 1px solid {ACTIVEBORDER};
    border-top: 1px solid {ACTIVEBORDER};
    border-right: 1px solid {ACTIVEBORDER};
}}

QTabBar::tab:selected,
QTabBar::tab:hover {{
    border-bottom: None;
    background-color: {WINDOW};
}}

QTabBar::tab:selected {{
    top: 1px;
    border-bottom: None;
}}

QHeaderView {{
    font-weight: bold;
}}
"""
