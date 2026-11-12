from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox,
)
from database import COLUMN_DEFS
from widgets.column import Column
from widgets.task_card import TaskCard


class BoardWidget(QWidget):
    def __init__(self, board_id, board_name, db, parent=None):
        super().__init__(parent)
        self.board_id = board_id
        self.board_name = board_name
        self.db = db

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        top = QHBoxLayout()
        self.title_label = QLabel(f"📋  {board_name}")
        self.title_label.setObjectName("TitleLabel")
        top.addWidget(self.title_label)
        top.addStretch()

        clear_btn = QPushButton("🗑  Очистить доску")
        clear_btn.clicked.connect(self.clear_board)
        top.addWidget(clear_btn)

        reset_btn = QPushButton("🔄  Сброс")
        reset_btn.clicked.connect(self.reset_board)
        top.addWidget(reset_btn)
        layout.addLayout(top)

        cols_layout = QHBoxLayout()
        cols_layout.setSpacing(12)
        layout.addLayout(cols_layout, 1)

        self.columns = {}
        for key, title, color in COLUMN_DEFS:
            col = Column(self.board_id, key, title, color, self.db)
            self.columns[key] = col
            cols_layout.addWidget(col)

    def load_tasks(self):
        for col in self.columns.values():
            col.load_tasks()

    def rename_to(self, new_name):
        self.db.rename_board(self.board_id, new_name)
        self.board_name = new_name
        self.title_label.setText(f"📋  {new_name}")

    def clear_board(self, silent=False):
        if not silent:
            reply = QMessageBox.question(
                self, "Очистить доску",
                f"Удалить все задачи на доске «{self.board_name}»?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        for col in self.columns.values():
            self.db.clear_column(col.db_column_id)
            for i in reversed(range(col.tasks_layout.count())):
                w = col.tasks_layout.itemAt(i).widget()
                if isinstance(w, TaskCard):
                    col.tasks_layout.removeWidget(w)
                    w.deleteLater()
            col.update_count()

    def reset_board(self):
        reply = QMessageBox.question(
            self, "Сброс доски",
            "Загрузить демо-данные? Текущие задачи будут заменены.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.clear_board(silent=True)
            todo = self.columns["todo"]
            self.db.add_task(
                todo.db_column_id, "Пример задачи",
                "Перетащи меня в другую колонку →",
            )
            todo.load_tasks()