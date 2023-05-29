from flask import Flask, render_template, request, url_for, redirect, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wfou200ef2h0ehf2eij1-fi2h2'


def get_db_connection():
    connection = sqlite3.connect('database.db')
    return connection


@app.route('/')
def index():
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute('SELECT * FROM "articles";')
    articles = cur.fetchall()
    cur.close()
    connection.close()
    return render_template("index.html", articles=articles)


@app.route('/authorization', methods=('GET', 'POST'))
def authorization():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute('SELECT * FROM "users";')
        users = cur.fetchall()
        for user in users:
            if email == user[2] and check_password_hash(user[3], password):
                return redirect(url_for('create'))
            else:
                flash("Не верный логин или пароль!")

    return render_template('authorization.html')


@app.route('/registration', methods=('GET', 'POST'))
def registration():
    if request.method == 'POST':
        if len(request.form['nickname']) > 4 and len(request.form['email']) > 4 \
                and len(request.form['password']) > 4 and request.form['password'] == request.form['password2']:
            nickname = request.form['nickname']
            email = request.form['email']
            hash = generate_password_hash(request.form['password'])

            connection = get_db_connection()
            cur = connection.cursor()
            cur.execute(f"SELECT email FROM users WHERE email LIKE ?;", (email,))
            res = cur.fetchone()
            if res is None:
                cur.execute('INSERT INTO users (nickname, email, password)'
                            'VALUES (?, ?, ?)',
                            (nickname,
                             email,
                             hash)
                            )
                connection.commit()
                cur.close()
                connection.close()
                return redirect(url_for('authorization'))
            else:
                flash("Ошибка! Возможны 3 причины: 1)Пользователь с таким email уже есть. 2)Длинна полей меньше 4. 3)Пароли не совпадают.")

    return render_template('registration.html')


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute('INSERT INTO articles (title, author, content)'
                    'VALUES (?, ?, ?)',
                    (title,
                     author,
                     content)
                    )
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('index'))
    return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)
