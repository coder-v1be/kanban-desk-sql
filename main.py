import sys
from PyQt6.QtWidgets import QApplication

from database import Database, DB_PATH
from window import KanbanWindow


def main():
    db = Database(DB_PATH)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = KanbanWindow(db)
    window.show()
    try:
        sys.exit(app.exec())
    finally:
        db.conn.close()


if __name__ == "__main__":
    main()