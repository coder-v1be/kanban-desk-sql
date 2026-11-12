from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QInputDialog, QMessageBox, QMenu,
)
from PyQt6.QtCore import Qt

from style import DARK_STYLE
from widgets.board import BoardWidget

class KanbanWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Kanban Board — SQLite")
        self.resize(1400, 800)
        self.setStyleSheet(DARK_STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 8)

        top = QHBoxLayout()
        title = QLabel("📋  Канбан-доски")
        title.setObjectName("TitleLabel")
        top.addWidget(title)
        top.addStretch()
        new_btn = QPushButton("＋  Новая доска")
        new_btn.setObjectName("AddBtn")
        new_btn.clicked.connect(self.create_new_board_dialog)
        top.addWidget(new_btn)
        layout.addLayout(top)

        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.tab_context_menu)
        self.tabs.tabBarDoubleClicked.connect(self.rename_tab_dialog)
        layout.addWidget(self.tabs, 1)

        self.load_boards()

    def load_boards(self):
        boards = self.db.all_boards()
        if not boards:
            bid = self.db.create_board("Моя доска")
            boards = [(bid, "Моя доска")]
        for bid, name in boards:
            self._add_tab(bid, name)
        self.tabs.setCurrentIndex(0)

    def _add_tab(self, board_id, name):
        board = BoardWidget(board_id, name, self.db)
        board.load_tasks()
        idx = self.tabs.addTab(board, name)
        self.tabs.setCurrentIndex(idx)
        return board

    def create_new_board_dialog(self):
        name, ok = QInputDialog.getText(
            self, "Новая доска", "Название доски:", text="Новая доска"
        )
        if ok and name.strip():
            self.create_new_board(name.strip())

    def create_new_board(self, name):
        base, i = name, 1
        existing = [self.tabs.tabText(k) for k in range(self.tabs.count())]
        while name in existing:
            i += 1
            name = f"{base} ({i})"
        bid = self.db.create_board(name)
        self._add_tab(bid, name)

    def rename_tab_dialog(self, index):
        if index < 0:
            return
        board = self.tabs.widget(index)
        new_name, ok = QInputDialog.getText(
            self, "Переименовать доску", "Новое название:",
            text=board.board_name,
        )
        if ok and new_name.strip() and new_name.strip() != board.board_name:
            board.rename_to(new_name.strip())
            self.tabs.setTabText(index, new_name.strip())

    def tab_context_menu(self, pos):
        index = self.tabs.tabBar().tabAt(pos)
        if index < 0:
            return
        menu = QMenu(self)
        rename_a = menu.addAction("✏  Переименовать")
        close_a = menu.addAction("✕  Закрыть доску")
        menu.addSeparator()
        new_a = menu.addAction("＋  Новая доска")
        action = menu.exec(self.tabs.tabBar().mapToGlobal(pos))
        if action == rename_a:
            self.rename_tab_dialog(index)
        elif action == close_a:
            self.close_tab(index)
        elif action == new_a:
            self.create_new_board_dialog()

    def close_tab(self, index):
        board = self.tabs.widget(index)
        if self.tabs.count() == 1:
            reply = QMessageBox.question(
                self, "Закрыть последнюю доску",
                "Это последняя доска. Удалить её вместе с задачами?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
            self.db.delete_board(board.board_id)
        else:
            reply = QMessageBox.question(
                self, "Закрыть доску",
                f"Закрыть доску «{board.board_name}»?\n"
                "Задачи останутся в базе и появятся снова при следующем запуске.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        self.tabs.removeTab(index)
        board.deleteLater()