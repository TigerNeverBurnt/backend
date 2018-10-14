from flask import Flask


def create_app():
    app = Flask(__name__)
    return app


application = create_app()

if __name__ == '__main__':
    application.run()
