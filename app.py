from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "IMPORTEXPORT_STARTUP_2026"

DB_FILE = "database/users.json"

def load_users():
    with open(DB_FILE) as f:
        return json.load(f)

def save_users(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form['username']
        p = request.form['password']

        users = load_users()
        for user in users:
            if user['username'] == u and user['password_hash'] == p:
                session['user'] = u
                session['role'] = user['role']
                return redirect("/dashboard")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form['username']
        p = request.form['password']

        users = load_users()
        users.append({
            "username": u,
            "password_hash": p,
            "role": "staff",
            "created_at": datetime.now().strftime("%Y-%m-%d")
        })
        save_users(users)
        return redirect("/")
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect("/")
    return render_template("dashboard.html", user=session['user'])


@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/")
    users = load_users()
    return render_template("admin.html", users=users)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
