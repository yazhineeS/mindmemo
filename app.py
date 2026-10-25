from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
#app.secret_key = "yoursecretkey"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(BASE_DIR, "mindmemo.db") 
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

def get_db():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            entry TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()


def load_entries(user_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT id, entry, timestamp FROM entries WHERE user_id = ? ORDER BY id DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def save_entry(user_id, entry):
    conn = get_db()
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M]")
    conn.execute(
        "INSERT INTO entries (user_id, entry, timestamp) VALUES (?, ?, ?)",
        (user_id, entry, timestamp),
    )
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        action = request.form.get("action", "login")
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return render_template("login.html", error="Username and password are required", active_tab=action)

        conn = get_db()

        if action == "signup":
            existing = conn.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone()
            if existing:
                conn.close()
                return render_template("login.html", error="That username is already taken", active_tab="signup")

            hashed = generate_password_hash(password)
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed),
            )
            conn.commit()
            user = conn.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone()
            conn.close()

            session["user"] = username
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        else:
            user = conn.execute(
                "SELECT id, password FROM users WHERE username = ?", (username,)
            ).fetchone()
            conn.close()

            if user and check_password_hash(user["password"], password):
                session["user"] = username
                session["user_id"] = user["id"]
                return redirect(url_for("index"))
            else:
                return render_template("login.html", error="Invalid username or password", active_tab="login")

    return render_template("login.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        entry = request.form.get("entry", "").strip()
        if entry:
            save_entry(session["user_id"], entry)
        return redirect(url_for("index"))

    entries = load_entries(session["user_id"])
    return render_template("index.html", entries=entries, username=session.get("user"))


@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete_entry_route(entry_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    # Only delete if the entry actually belongs to the logged-in user
    conn.execute(
        "DELETE FROM entries WHERE id = ? AND user_id = ?",
        (entry_id, session["user_id"]),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

init_db()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1") 


