import os, ConfigParser
from flask import Flask, jsonify, request
import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
         SECRET_KEY='dev',
         DATABASE=os.path.join(app.instance_path, 'game.db'),
    )
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/login', methods=["GET"])
    def login():
        try:
            db_items = db.get_db().execute("SELECT name, price FROM items").fetchall()
            server_items = []
            for it in db_items:
                print(list(zip(it.keys(), it)) )
                server_items.append(list(zip(it.keys(), it)))

            username = request.headers.get('username')
            users = db.get_db().execute("SELECT login,credit FROM users WHERE login = ?", (username,)).fetchone()
            if users is None:
                users = db.get_db().execute("INSERT INTO users(login, credit) VALUES(?,?)", (username, 0))
                db.get_db().commit()
            else:
                db.get_db().execute("UPDATE users SET credit = ? WHERE login=?;", (int(users['credit'])+100, users['login']))
                db.get_db().commit()
            return jsonify( username=username,
                            credit=users['credit'],
                            items=server_items)
        except:
            return jsonify(error="Error authorisation")

    @app.route('/logout', methods=["GET"])
    def logout():
        error = None
        user = request.headers.get('username')
        return jsonify()

    @app.route('/sell', methods=["GET"])
    def sell():
        try:
            item = str(request.args.get('item'))
            user = request.headers.get('username')
            print("User " + user + " try to sell " + str(item))
            return jsonify()
        except:
            return jsonify(error="Error sell item")


    @app.route('/buy', methods=["GET"])
    def buy():
        try:
            item = str(request.args.get('item'))
            user = request.headers.get('username')
            print("User "+user+" try to buy "+str(item))
            return jsonify()
        except:
            return jsonify(error="Error sell item")

    @app.route('/get_items', methods=["GET"])
    def get_items():
        try:
            return jsonify(items=server_items)
        except:
            return jsonify(error="Error sell item")

    db.init_app(app)

    return app