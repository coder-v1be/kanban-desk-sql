from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMenu,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QMimeData, QPoint, pyqtSignal
from PyQt6.QtGui import QDrag, QPixmap, QPainter, QColor, QFont, QCursor


class TaskCard(QFrame):
    delete_requested = pyqtSignal(object)
    edit_requested = pyqtSignal(object)

    def __init__(self, task_id, title, description, parent_column, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.title = title
        self.description = description
        self.parent_column = parent_column
        self.drag_start_pos = QPoint()

        self.setObjectName("TaskCard")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 8, 8, 8)
        self.main_layout.setSpacing(4)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        self.title_label = QLabel(title)
        self.title_label.setObjectName("TaskTitle")
        self.title_label.setWordWrap(True)
        header.addWidget(self.title_label, 1)

        delete_btn = QPushButton("✕")
        delete_btn.setObjectName("DeleteBtn")
        delete_btn.setFixedSize(22, 22)
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self))
        header.addWidget(delete_btn)
        self.main_layout.addLayout(header)

        self.desc_label = QLabel(description)
        self.desc_label.setObjectName("TaskDesc")
        self.desc_label.setWordWrap(True)
        self.main_layout.addWidget(self.desc_label)
        if not description:
            self.desc_label.hide()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        edit_action = menu.addAction("✏  Редактировать")
        delete_action = menu.addAction("🗑  Удалить")
        action = menu.exec(self.mapToGlobal(pos))
        if action == edit_action:
            self.edit_requested.emit(self)
        elif action == delete_action:
            self.delete_requested.emit(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if (event.position().toPoint() - self.drag_start_pos).manhattanLength() < 10:
            return

        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(str(self.task_id))
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("#45475a"))
        painter.setPen(QColor("#89b4fa"))
        painter.drawRoundedRect(pixmap.rect().adjusted(1, 1, -1, -1), 8, 8)
        painter.setPen(QColor("#cdd6f4"))
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        painter.drawText(
            pixmap.rect().adjusted(12, 0, -12, 0),
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
            self.title,
        )
        painter.end()
        drag.setMimeData(mime)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.position().toPoint())
        drag.exec(Qt.DropAction.MoveAction)