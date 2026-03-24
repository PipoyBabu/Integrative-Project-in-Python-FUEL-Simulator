from flask import Flask, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="fleet_db"
)

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return "no_user"

    if user["password"] != password:
        return "wrong_password"

    return "success"


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("fullname")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        return "empty"

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    
    if cursor.fetchone():
        return "exists"

    cursor.execute(
        "INSERT INTO users (fullname, email, password) VALUES (%s,%s,%s)",
        (name, email, password)
    )
    db.commit()

    return "success"


if __name__ == "__main__":
    app.run(debug=True)