import os, ConfigParser, random
from flask import Flask, jsonify, request
import db
def read_config(config_path):
    server_items = {}
    try:
        Config = ConfigParser.ConfigParser()
        Config.read(config_path)
        for section in Config.sections():
            options = Config.options(section)
            for option in options:
                try:
                    server_items[option] = Config.get(section, option)
                    if server_items[option] == -1:
                        print("skip: %s" % option)
                except:
                    print("exception on %s!" % option)
                    server_items[option] = None
        return server_items
    except:
        print "Error reading file with items"
        return {}


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

    game_config = read_config("config.txt")

    @app.route('/login', methods=["GET"])
    def login():
        try:
            username = request.headers.get('username')
            random_credit_bonus = random.randint(1, int(game_config['limit_random_credit']))
            user = db.get_user(username, random_credit_bonus)
            server_items = db.get_user_items(username)
            return jsonify( username=username,
                            credit=user['credit']+random_credit_bonus,
                            items=server_items,
                            message_credit=random_credit_bonus)
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