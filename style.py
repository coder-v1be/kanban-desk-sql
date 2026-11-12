DARK_STYLE = """
QMainWindow, QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13px;
}
QLabel#TitleLabel {
    color: #89b4fa;
    font-size: 22px;
    font-weight: bold;
    padding: 8px;
}
QLabel#ColumnTitle {
    color: #f5e0dc;
    font-size: 15px;
    font-weight: bold;
    padding: 6px;
}
QLabel#CountBadge {
    background-color: #45475a;
    color: #cdd6f4;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: bold;
}
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #45475a;
    border-color: #89b4fa;
}
QPushButton:pressed {
    background-color: #585b70;
}
QPushButton#AddBtn {
    background-color: #89b4fa;
    color: #1e1e2e;
    font-weight: bold;
}
QPushButton#AddBtn:hover {
    background-color: #b4befe;
}
QPushButton#DeleteBtn {
    background-color: transparent;
    color: #f38ba8;
    border: none;
    padding: 2px 6px;
    font-size: 14px;
}
QPushButton#DeleteBtn:hover {
    color: #eba0ac;
    background-color: #45475a;
    border-radius: 4px;
}
QFrame#Column {
    background-color: #181825;
    border-radius: 10px;
    border: 1px solid #313244;
}
QFrame#TaskCard {
    background-color: #313244;
    border-radius: 8px;
    border-left: 4px solid #89b4fa;
}
QFrame#TaskCard:hover {
    background-color: #45475a;
}
QLabel#TaskTitle {
    color: #cdd6f4;
    font-weight: 600;
    font-size: 13px;
}
QLabel#TaskDesc {
    color: #a6adc8;
    font-size: 11px;
}
QScrollArea {
    background-color: transparent;
    border: none;
}
QScrollBar:vertical {
    background: #181825;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #45475a;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #585b70;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QLineEdit, QTextEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #89b4fa;
}
QMenu {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 20px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #45475a;
}
QDialog {
    background-color: #1e1e2e;
}
QTabWidget::pane {
    border: 1px solid #313244;
    border-radius: 8px;
    background-color: #1e1e2e;
    top: -1px;
}
QTabBar::tab {
    background-color: #313244;
    color: #a6adc8;
    border: 1px solid #313244;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 8px 18px;
    margin-right: 3px;
    font-weight: 500;
}
QTabBar::tab:selected {
    background-color: #1e1e2e;
    color: #89b4fa;
    border-bottom: 2px solid #89b4fa;
}
QTabBar::tab:hover:!selected {
    background-color: #45475a;
    color: #cdd6f4;
}
"""
