from financespy_web.transactions import transactions_blueprint
from flask import Flask
from financespy.account import open_account


def create_app(config):
    app = Flask(__name__)

    account = open_account('/home/danilo/Documents/finances/bank')

    app.register_blueprint(transactions_blueprint(account, __name__))

    return app
