from flask import Flask
from interface import interface


engine = Flask(__name__)
engine.register_blueprint(interface, url_prefix="/")


if __name__ == '__main__':
    engine.run(debug=True, port=8000)