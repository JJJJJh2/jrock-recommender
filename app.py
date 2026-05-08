import sqlite3
import os
from datetime import datetime, timezone, timedelta

from flask import Flask, render_template, request

from bands_data import recommend, get_suggestions

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.db")
JST = timezone(timedelta(hours=9))


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                matched_band TEXT,
                results TEXT,
                created_at TEXT NOT NULL
            )
        """)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").strip()
    if not query:
        return render_template("index.html", error="请输入乐队名 / Please enter a band name.")

    matched, results, quality = recommend(query)

    if not matched:
        suggestions = get_suggestions(query)
        if suggestions:
            names = " / ".join(f"「{s}」" for s in suggestions[:3])
            hint = f"你是不是想搜：{names}"
        else:
            hint = "试试：SUPERCAR / きのこ帝国 / envy / tricot / toe / Mono …"
        return render_template(
            "index.html",
            query=query,
            error=f"找不到「{query}」的信息。{hint}",
        )

    now = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    with get_db() as conn:
        conn.execute(
            "INSERT INTO history (query, matched_band, results, created_at) VALUES (?, ?, ?, ?)",
            (query, matched["name"], ",".join(r["name"] for r in results), now),
        )

    return render_template("index.html", query=query, matched=matched, results=results)


@app.route("/history")
def history():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM history ORDER BY id DESC LIMIT 50"
        ).fetchall()
    return render_template("history.html", rows=rows)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
