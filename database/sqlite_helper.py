# database/sqlite_helper.py
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data") / "sentiment_history.db"


def get_connection():
    """Tạo kết nối đến SQLite, tự tạo thư mục nếu chưa có."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Khởi tạo bảng SQLite nếu chưa tồn tại."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sentiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def insert_record(text: str, sentiment: str):
    """Lưu một bản ghi phân loại cảm xúc."""
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO sentiments (text, sentiment, timestamp)
        VALUES (?, ?, ?);
        """,
        (text, sentiment, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()


def get_history(limit: int = 50):
    """Lấy 50 bản ghi mới nhất để hiển thị lên UI."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, text, sentiment, timestamp
        FROM sentiments
        ORDER BY timestamp DESC
        LIMIT ?;
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def clear_history():
    """Xóa toàn bộ lịch sử phân loại cảm xúc."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM sentiments")  # ĐÃ SỬA: sentiments, không phải sentiment_history
        conn.commit()
        cur.execute("VACUUM")
        conn.commit()
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            pass  # Lần đầu chạy → chưa có bảng → bỏ qua
        else:
            raise
    finally:
        conn.close()