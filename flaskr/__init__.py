from dotenv import load_dotenv

from flask import Flask, redirect, render_template, url_for

load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template('base.html')


    return app