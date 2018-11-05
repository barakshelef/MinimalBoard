import os
import sqlite3

from flask import Flask, g, render_template

app = Flask(__name__)

if not os.path.isdir(app.instance_path):
    os.mkdir(app.instance_path)

DATABASE = os.path.join(app.instance_path, 'db.sqlite')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)

    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute("DROP TABLE IF EXISTS post;")
    db.execute("CREATE TABLE post ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT, "
               "date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "
               "msg TEXT NOT NULL"
               ");")


@app.route('/')
def index():
    db = get_db()
    posts = db.execute("SELECT msg, date FROM post ORDER BY date DESC").fetchall()
    return render_template('index.html', posts=posts)


@app.route("/init")
def init_db_route():
    init_db()
    return "DB Initialized"
