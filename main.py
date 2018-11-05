import os
import sqlite3

from flask import Flask, g

app = Flask(__name__)

if not os.path.isdir(app.instance_path):
    os.mkdir(app.instance_path)

DATABASE=os.path.join(app.instance_path, 'db.sqlite')


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
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS post;")
    c.execute("CREATE TABLE post ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT, "
              "date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "
              "msg TEXT NOT NULL"
              ");")
    db.commit()
    close_db()

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/init")
def init_db_route():
    init_db()
    return "DB Initialized"