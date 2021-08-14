import os
import bcrypt

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
from flaskext.mysql import MySQL
from dotenv import load_dotenv
from datetime import datetime


app = Flask(__name__)


# Dotenv (MySQL Password)
load_dotenv()
DB_HOST = os.getenv("MYSQL_HOST")
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_DATABASE = os.getenv("MYSQL_DATABASE")
SECRET = os.getenv("SECRET_KEY")

# Flask and secret key
app = Flask(__name__)
app.secret_key = SECRET

# Database Settings
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = DB_HOST
app.config['MYSQL_DATABASE_USER'] = DB_USER
app.config['MYSQL_DATABASE_PASSWORD'] = DB_PASSWORD
app.config['MYSQL_DATABASE_DB'] = DB_DATABASE
mysql.init_app(app)

# Seed for encrypting
seed = bcrypt.gensalt()

DIRECTORY = os.path.join("uploads")
app.config["DIRECTORY"] = DIRECTORY


@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == 'GET'):
        if "name" in session:
            return render_template("index.html")
        else:
            return render_template("register.html")
    else:
        name = request.form["nameRegister"]
        email = request.form["emailRegister"]
        password = request.form["passwordRegister"]
        password_encode = password.encode("utf-8")
        password_encrypt = bcrypt.hashpw(password_encode, seed)

        if name == "" or email == "" or password == "":
            flash("Please enter all required fields")
            return redirect(url_for("register"))

        # SQL Query
        sql = "INSERT INTO users (email, password, name) VALUES (%s, %s, %s)"

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(sql, (email, password_encrypt, name))
        conn.commit()

        session["name"] = name
        # session["email"] = _email

        return redirect(url_for("index"))


@app.route('/login', methods=['GET'])
def login():
    if (request.method == 'GET'):
        if "name" in session:
            return render_template("index.html")
        else:
            return render_template("login.html")


@app.route("/signin", methods=['POST'])
def signin():
    _email = request.form["emailLogin"]
    _password = request.form["passwordLogin"]
    _password_encode = _password.encode("utf-8")

    sql = "SELECT email, password FROM users WHERE email = %s"

    data = [_email]

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(sql, data)
    user = cur.fetchone()
    conn.close()

    if (user != None):
        _password_encrypt_encode = user[1].encode()

        if (bcrypt.checkpw(_password_encode, _password_encrypt_encode)):

            session["name"] = user[1][1]
            redirect(url_for("index"))
        else:
            flash("Incorrect Password!")
            return render_template("login.html")
    else:
        flash("Email does not exist!")
        return render_template("login.html")
    return redirect(url_for("index"))


@app.route('/uploads/<namePhoto>')
def uploads(namePhoto):
    return send_from_directory(app.config["DIRECTORY"], namePhoto)


@app.route("/")
def main():
    if "name" in session:
        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))


@app.route('/exit')
def exit1():
    session.clear()
    return redirect(url_for("login"))


@app.route("/home")
def index():
    if "name" in session:
        sql = "SELECT * FROM system;"

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(sql)
        employees = cur.fetchall()

        conn.commit()
        return render_template("index.html", employees=employees)
    else:
        return render_template("login.html")


@app.route('/delete/<int:id>')
def delete(id):
    if "name" in session:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT photo FROM system WHERE id = %s", id)
        rows = cur.fetchall()

        os.remove(os.path.join(app.config["DIRECTORY"], rows[0][0]))
        cur.execute("DELETE FROM system WHERE id = %s", {id})

        flash("Employee has been deleted successfully!")
        conn.commit()
        return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route('/edit/<int:id>')
def edit(id):
    if "name" in session:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM system WHERE id = %s", {id})
        employees = cur.fetchall()

        conn.commit()

        return render_template("edit.html", employees=employees)
    else:
        return render_template("login.html")


@app.route('/update', methods=['POST'])
def update():
    _name = request.form["name"]
    _email = request.form["email"]

    _photo = request.files["photo"]

    id = request.form["inputID"]

    sql = "UPDATE system SET name = %s, email = %s WHERE id = %s;"

    data = (_name, _email, id)

    conn = mysql.connect()
    cur = conn.cursor()

    now = datetime.now()
    time = now.strftime("%Y%H%M%S")

    if _photo.filename != "":

        newNamePhoto = time + _photo.filename
        _photo.save("uploads/" + newNamePhoto)

        cur.execute("SELECT photo FROM system WHERE id = %s", id)
        rows = cur.fetchall()

        os.remove(os.path.join(app.config["DIRECTORY"], rows[0][0]))
        cur.execute("UPDATE system SET photo = %s WHERE id = %s",
                    (newNamePhoto, id))
        conn.commit()

    cur.execute(sql, data)

    flash("Employee has been updated successfully!")
    conn.commit()

    return redirect(url_for("index"))


@app.route('/create')
def create():
    return render_template("create.html")


@app.route('/store', methods=['POST'])
def storage():
    _name = request.form["name"]
    _email = request.form["email"]

    _photo = request.files["photo"]

    if _name == "" or _email == "" or _photo == "":
        flash("Please enter all required fields")
        return redirect(url_for("create"))

    now = datetime.now()
    time = now.strftime("%Y%H%M%S")

    if _photo.filename != "":
        newNamePhoto = time + _photo.filename
        _photo.save("uploads/" + newNamePhoto)

    sql = "INSERT INTO system (id, name, email, photo) VALUES (NULL, %s, %s, %s)"

    data = (_name, _email, newNamePhoto)

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(sql, data)

    flash("Employee has been created successfully!")
    conn.commit()

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
