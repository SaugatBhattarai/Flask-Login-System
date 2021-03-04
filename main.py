from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.secret_key = "234343"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "login"

db = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    # print('Login Success Status', session['loginsuccess'])
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "SELECT * FROM logininfo WHERE email=%s AND password=%s", (username, password))
            info = cursor.fetchone()
            print(info)
            if info is not None:
                if info['email'] == username and info['password'] == password:
                    session['loginsuccess'] = True
                    session['username'] = username
                    return redirect(url_for('profile'))
            else:
                return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    # if session['loginsuccess'] == True:
    #     # session['loginsuccess'] = False
    #     return redirect(url_for('index'))
    session.pop('loginsuccess', None)
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if session['loginsuccess'] == True:
        username = session['username']
        return render_template("profile.html", username=username)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        if "name" in request.form and "email" in request.form and "password" in request.form:
            username = request.form['name']
            email = request.form['email']
            password = request.form['password']
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO login.logininfo(name,email,password) VALUES(%s,%s,%s)",
                        (username, email, password))
            db.connection.commit()
            return redirect(url_for('index'))
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)
