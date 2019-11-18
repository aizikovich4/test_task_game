import sqlite3

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext


def get_items():
    try:
        db_items = get_db().execute("SELECT name, price FROM items").fetchall()
        server_items = []
        for it in db_items:
            server_items.append(list(zip(it.keys(), it)))
        return server_items
    except:
        print("Get get_items")
        return []


def get_user_items(username):
    try:
        user = get_db().execute("SELECT id_user FROM users WHERE login = ?", (username,)).fetchone()
        if user is None:
            return []
        items = get_db().execute("SELECT item_id FROM user_items WHERE user_id = ?", (user['id_user'],)).fetchall()

        if items is not None:
            user_items = []
            for it in items:
                db_item = get_db().execute("SELECT name, price FROM items  WHERE id_item = ?", (it['item_id'],)).fetchone()
                user_items.append([db_item['name'], db_item['price'] ])
            return user_items
        else:
            return []
    except:
        print ("Error get_user_items")
        return []

def get_user(username):
    try:
        user = get_db().execute("SELECT login,credit FROM users WHERE login = ?", (username,)).fetchone()
        if user is None:
            user = create_new_user(username)
        else:
            get_db().execute("UPDATE users SET credit = ? WHERE login=?;",
                                (int(user['credit']) + 100, user['login']))
            get_db().commit()
        return user
    except:
        print("Get get_user")
        return


def create_new_user(username):
    try:
        get_db().execute("INSERT INTO users(login, credit) VALUES(?,?)", (username, 0))
        get_db().commit()
        return {'credit': 0}
    except:
        print("Get create_new_user")
        return []

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect("game.db")
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
