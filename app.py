from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import date

app = Flask(__name__)
app.secret_key = "task_collaboration_secret_key"

DATABASE = "tasks.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
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
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Pending',
            deadline TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    columns = [
        row["name"]
        for row in conn.execute("PRAGMA table_info(tasks)").fetchall()
    ]

    if "deadline" not in columns:
        conn.execute("ALTER TABLE tasks ADD COLUMN deadline TEXT")

    conn.commit()
    conn.close()


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            conn.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists.", "error")
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "").strip()

    conn = get_db()

    query = "SELECT * FROM tasks WHERE user_id = ?"
    params = [session["user_id"]]

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    if status_filter in ["Pending", "In Progress", "Completed"]:
        query += " AND status = ?"
        params.append(status_filter)

    query += """
        ORDER BY
        CASE WHEN deadline IS NULL OR deadline = '' THEN 1 ELSE 0 END,
        deadline ASC,
        id DESC
    """

    tasks = conn.execute(query, params).fetchall()

    stats = conn.execute("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) AS pending,
            SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
            SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed
        FROM tasks
        WHERE user_id = ?
    """, (session["user_id"],)).fetchone()

    conn.close()

    return render_template(
        "dashboard.html",
        tasks=tasks,
        stats=stats,
        search=search,
        status_filter=status_filter,
        today=date.today().isoformat()
    )


@app.route("/add_task", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    deadline = request.form.get("deadline", "").strip()

    if not title:
        flash("Task title is required.", "error")
        return redirect(url_for("dashboard"))

    conn = get_db()
    conn.execute("""
        INSERT INTO tasks (user_id, title, description, status, deadline)
        VALUES (?, ?, ?, 'Pending', ?)
    """, (
        session["user_id"],
        title,
        description,
        deadline or None
    ))
    conn.commit()
    conn.close()

    flash("Task added successfully.", "success")
    return redirect(url_for("dashboard"))


@app.route("/update_status/<int:task_id>", methods=["POST"])
@login_required
def update_status(task_id):
    status = request.form.get("status")

    if status not in ["Pending", "In Progress", "Completed"]:
        flash("Invalid task status.", "error")
        return redirect(url_for("dashboard"))

    conn = get_db()
    cursor = conn.execute("""
        UPDATE tasks
        SET status = ?
        WHERE id = ? AND user_id = ?
    """, (status, task_id, session["user_id"]))

    conn.commit()
    conn.close()

    if cursor.rowcount:
        flash("Task status updated.", "success")
    else:
        flash("Task not found.", "error")

    return redirect(url_for("dashboard"))


@app.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    conn = get_db()
    cursor = conn.execute("""
        DELETE FROM tasks
        WHERE id = ? AND user_id = ?
    """, (task_id, session["user_id"]))

    conn.commit()
    conn.close()

    if cursor.rowcount:
        flash("Task deleted successfully.", "success")
    else:
        flash("Task not found.", "error")

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

