import os
from flask import Flask, jsonify, request

def create_server(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'test_game.sqlite'),
    )

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/login', methods=["GET"])
    def login():
        error = None
        user = request.headers.get('username')
        login = user
        return jsonify(username=login, credit=100)

    @app.route('/logout', methods=["GET"])
    def logout():
        error = None
        user = request.headers.get('username')
        return jsonify()

    @app.route('/sell', methods=["GET"])
    def sell():
        item = str(request.args.get('item'))
        user = request.headers.get('username')
        print("User " + user + " try to sell " + str(item))
        return jsonify()

    @app.route('/buy', methods=["GET"])
    def buy():
        error = None
        item = str(request.args.get('item'))
        user = request.headers.get('username')
        print("User "+user+" try to buy "+str(item))
        return jsonify()

    return app


if __name__ == '__main__':
    app = create_server()
    app.run(host='0.0.0.0', port=5000, debug=True, load_dotenv=False)
