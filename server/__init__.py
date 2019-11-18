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
            username = request.headers.get('username')

            server_items = db.get_user_items(username)
            user = db.get_user(username)
            return jsonify( username=username,
                            credit=user['credit']+100,
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
            username = request.headers.get('username')
            print("User " + username + " try to sell " + str(item))
            err = db.sell_item(username, item)

            if err is not None:
                return jsonify(error=err)

            server_items = db.get_user_items(username)
            user = db.get_user(username)
            return jsonify(credit=user['credit'],
                           items=server_items)
        except:
            return jsonify(error="Error sell item")


    @app.route('/buy', methods=["GET"])
    def buy():
        try:
            item = str(request.args.get('item'))
            username = str(request.headers.get('username'))
            print("User " + username + " try to buy "+str(item))
            err = db.buy_item(username, item)

            if err is not None:
                return jsonify(error=err)

            server_items = db.get_user_items(username)
            user = db.get_user(username)
            return jsonify(credit=user['credit'],
                            items=server_items)
        except:
             return jsonify(error="Error buy item")

    @app.route('/get_items', methods=["GET"])
    def get_items():
        try:
            server_items = db.get_items()
            return jsonify(items=server_items)
        except:
            return jsonify(error="Error get item")

    db.init_app(app)

    return app