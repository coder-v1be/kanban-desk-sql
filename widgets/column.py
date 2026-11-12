from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QDialog,
)
from PyQt6.QtCore import Qt

from dialogs import TaskDialog
from widgets.task_card import TaskCard


class Column(QFrame):
    def __init__(self, board_id, column_key, title, color, db, parent=None):
        super().__init__(parent)
        self.board_id = board_id
        self.column_key = column_key
        self.title = title
        self.color = color
        self.db = db
        self.db_column_id = db.column_id(board_id, column_key)

        self.setObjectName("Column")
        self.setAcceptDrops(True)
        self.setMinimumWidth(280)
        self.setMaximumWidth(340)

        main = QVBoxLayout(self)
        main.setContentsMargins(8, 8, 8, 8)
        main.setSpacing(8)

        header = QHBoxLayout()
        tlabel = QLabel(title)
        tlabel.setObjectName("ColumnTitle")
        tlabel.setStyleSheet(f"color: {color};")
        header.addWidget(tlabel)
        self.count_label = QLabel("0")
        self.count_label.setObjectName("CountBadge")
        header.addWidget(self.count_label)
        header.addStretch()
        main.addLayout(header)

        self.tasks_widget = QWidget()
        self.tasks_layout = QVBoxLayout(self.tasks_widget)
        self.tasks_layout.setContentsMargins(0, 0, 0, 0)
        self.tasks_layout.setSpacing(6)
        self.tasks_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.tasks_widget)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main.addWidget(scroll, 1)

        add_btn = QPushButton("＋  Добавить задачу")
        add_btn.setObjectName("AddBtn")
        add_btn.clicked.connect(self.add_task_dialog)
        main.addWidget(add_btn)

    def add_task_widget(self, card: TaskCard):
        card.delete_requested.connect(self.remove_task)
        card.edit_requested.connect(self.edit_task)
        self.tasks_layout.insertWidget(self.tasks_layout.count() - 1, card)
        self.update_count()

    def load_tasks(self):
        for task_id, title, description in self.db.tasks_for_column(self.db_column_id):
            card = TaskCard(task_id, title, description, self)
            self.add_task_widget(card)

    def update_count(self):
        count = sum(
            1 for i in range(self.tasks_layout.count())
            if isinstance(self.tasks_layout.itemAt(i).widget(), TaskCard)
        )
        self.count_label.setText(str(count))

    def add_task_dialog(self):
        dialog = TaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            title, desc = dialog.get_data()
            if title:
                tid = self.db.add_task(self.db_column_id, title, desc)
                self.add_task_widget(TaskCard(tid, title, desc, self))

    def remove_task(self, card: TaskCard):
        self.db.delete_task(card.task_id)
        self.tasks_layout.removeWidget(card)
        card.deleteLater()
        self.update_count()

    def edit_task(self, card: TaskCard):
        dialog = TaskDialog(self, card.title, card.description)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            title, desc = dialog.get_data()
            if title:
                self.db.update_task(card.task_id, title, desc)
                card.title = title
                card.description = desc
                card.title_label.setText(title)
                card.desc_label.setText(desc)
                card.desc_label.setVisible(bool(desc))

    # ----- drag&drop -----
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.setStyleSheet(
                f"QFrame#Column {{ background-color: #1e1e2e; "
                f"border: 1px solid {self.color}; }}"
            )

    def dragLeaveEvent(self, event):
        self.setStyleSheet("")

    def dropEvent(self, event):
        self.setStyleSheet("")
        source = event.source()
        if isinstance(source, TaskCard) and source.parent_column is not self:
            old = source.parent_column
            old.tasks_layout.removeWidget(source)
            source.setParent(None)
            source.parent_column = self
            self.db.move_task(source.task_id, self.db_column_id)
            self.add_task_widget(source)
            old.update_count()
            event.acceptProposedAction()