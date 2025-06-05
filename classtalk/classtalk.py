from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_classtalk():
        return 'Hello, Classtalk!'

    return app
