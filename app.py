from flask import Flask, render_template, request, redirect, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "IMPORTEXPORT_STARTUP_2026"

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "google_drive/service_account.json", scope)

client = gspread.authorize(creds)
sheet = client.open("IMPORT_EXPORT_USERS").sheet1


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form['username']
        p = request.form['password']
        for row in sheet.get_all_records():
            if row['username'] == u and check_password_hash(row['password_hash'], p):
                session['user'] = u
                session['role'] = row['role']
                return redirect("/dashboard")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form['username']
        p = generate_password_hash(request.form['password'])
        sheet.append_row([u, p, "staff", datetime.now().strftime("%Y-%m-%d")])
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
    return render_template("admin.html", users=sheet.get_all_records())


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


app.run(debug=True)
