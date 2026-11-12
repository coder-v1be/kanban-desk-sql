from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDialogButtonBox,
)
from style import DARK_STYLE


class TaskDialog(QDialog):
    def __init__(self, parent=None, title="", description=""):
        super().__init__(parent)
        self.setWindowTitle("Задача")
        self.setMinimumWidth(400)
        self.setStyleSheet(DARK_STYLE)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Название:"))
        self.title_edit = QLineEdit(title)
        self.title_edit.setPlaceholderText("Например: Сверстать лендинг")
        layout.addWidget(self.title_edit)

        layout.addWidget(QLabel("Описание:"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlainText(description)
        self.desc_edit.setPlaceholderText("Дополнительные детали...")
        self.desc_edit.setFixedHeight(100)
        layout.addWidget(self.desc_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return (
            self.title_edit.text().strip(),
            self.desc_edit.toPlainText().strip(),
        )
