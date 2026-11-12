import sqlite3

DB_PATH = "kanban.db"

COLUMN_DEFS = [
    ("todo", "📝  To Do", "#89b4fa"),
    ("in_progress", "⚙️  In Progress", "#fab387"),
    ("review", "👀  Review", "#cba6f7"),
    ("done", "✅  Done", "#a6e3a1"),
]


class Database:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_schema()

    def _create_schema(self):
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS boards (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                name     TEXT NOT NULL,
                position INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS columns (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                board_id INTEGER NOT NULL,
                key      TEXT NOT NULL,
                position INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                column_id   INTEGER NOT NULL,
                title       TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                position    INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (column_id) REFERENCES columns(id) ON DELETE CASCADE
            );
            """
        )
        self.conn.commit()

    # ---------- boards ----------
    def all_boards(self):
        return self.conn.execute(
            "SELECT id, name FROM boards ORDER BY position, id"
        ).fetchall()

    def create_board(self, name):
        cur = self.conn.cursor()
        pos = cur.execute(
            "SELECT COALESCE(MAX(position), -1) + 1 FROM boards"
        ).fetchone()[0]
        cur.execute(
            "INSERT INTO boards (name, position) VALUES (?, ?)", (name, pos)
        )
        board_id = cur.lastrowid
        for i, (key, _t, _c) in enumerate(COLUMN_DEFS):
            cur.execute(
                "INSERT INTO columns (board_id, key, position) VALUES (?, ?, ?)",
                (board_id, key, i),
            )
        self.conn.commit()
        return board_id

    def rename_board(self, board_id, new_name):
        self.conn.execute(
            "UPDATE boards SET name = ? WHERE id = ?", (new_name, board_id)
        )
        self.conn.commit()

    def delete_board(self, board_id):
        self.conn.execute("DELETE FROM boards WHERE id = ?", (board_id,))
        self.conn.commit()

    # ---------- columns ----------
    def column_id(self, board_id, key):
        row = self.conn.execute(
            "SELECT id FROM columns WHERE board_id = ? AND key = ?",
            (board_id, key),
        ).fetchone()
        return row[0] if row else None

    # ---------- tasks ----------
    def tasks_for_column(self, column_id):
        return self.conn.execute(
            "SELECT id, title, description FROM tasks "
            "WHERE column_id = ? ORDER BY position, id",
            (column_id,),
        ).fetchall()

    def add_task(self, column_id, title, description):
        cur = self.conn.cursor()
        pos = cur.execute(
            "SELECT COALESCE(MAX(position), -1) + 1 FROM tasks WHERE column_id = ?",
            (column_id,),
        ).fetchone()[0]
        cur.execute(
            "INSERT INTO tasks (column_id, title, description, position) "
            "VALUES (?, ?, ?, ?)",
            (column_id, title, description, pos),
        )
        self.conn.commit()
        return cur.lastrowid

    def update_task(self, task_id, title, description):
        self.conn.execute(
            "UPDATE tasks SET title = ?, description = ? WHERE id = ?",
            (title, description, task_id),
        )
        self.conn.commit()

    def delete_task(self, task_id):
        self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def move_task(self, task_id, new_column_id):
        cur = self.conn.cursor()
        pos = cur.execute(
            "SELECT COALESCE(MAX(position), -1) + 1 FROM tasks WHERE column_id = ?",
            (new_column_id,),
        ).fetchone()[0]
        cur.execute(
            "UPDATE tasks SET column_id = ?, position = ? WHERE id = ?",
            (new_column_id, pos, task_id),
        )
        self.conn.commit()

    def clear_column(self, column_id):
        self.conn.execute(
            "DELETE FROM tasks WHERE column_id = ?", (column_id,)
        )
        self.conn.commit()
