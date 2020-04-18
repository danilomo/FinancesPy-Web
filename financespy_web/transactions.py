import json
from flask import Response
from flask import Blueprint
from flask import request
from financespy import Transaction
from financespy import parse_month
from datetime import date


def month_weeks(backend, year, month):
    return [
        [trans.to_dict() for trans in week.records()]
        for week in backend.month(year=year, month=month).weeks()
    ]


def month_days(backend, year, month):
    return [
        [trans.to_dict() for trans in day.records()]
        for day in backend
        .month(year=year, month=month)
        .days()
    ]


def month_day(backend, year, month, day):
    return [
        trans.to_dict()
        for trans in backend
        .month(year=year, month=month)
        .day(day).records()
    ]


def transactions_blueprint(backend, name):
    transactions = Blueprint(
        "_transactions_",
        name,
        url_prefix="/api/accounts/<account>/transactions")

    @transactions.route("/")
    def root(user):
        return "It is working for " + user

    @transactions.route("/<int:year>/<month>", methods=("GET",))
    def month_all(account, year, month):
        result = [
            trans.to_dict()
            for trans in backend.month(year=year, month=month).records()
        ]

        return Response(
            json.dumps(result),
            mimetype="application/json"
        )

    @transactions.route("/<int:year>/<month>/<details>", methods=("GET",))
    def month_details(account, year, month, details):
        if details == "weeks":
            result = month_weeks(backend, year, month)
        elif details == "days":
            result = month_days(backend, year, month)
        else:
            result = month_day(backend, year, month, int(details))

        return Response(
            json.dumps(result),
            mimetype="application/json"
        )

    @transactions.route("/<int:year>/<month>/<int:day>", methods=("PUT",))
    def insert_record(account, year, month, day):
        payload = request.get_json()
        transaction = Transaction(
            value=payload["value"],
            description=payload["description"],
            categories=[]
        )

        backend.insert_record(
            date=date(year=year, month=parse_month(month), day=day),
            record=transaction
        )

        return ('', 204)

    return transactions
