from financespy_web import transactions_blueprint
from flask import Flask
from financespy import MemoryBackend
from financespy import categories
from financespy.transaction import parse_transaction
from datetime import datetime

records_ = """2019-09-04;20.0, withdrawal
2019-09-05;20.58, rewe
2019-09-06;49.28, aldi
2019-09-08;17.05, müller
2019-09-08;97.2, monthly_ticket
2019-09-11;50.0, withdrawal
2019-09-13;50.0, lidl
2019-09-19;40.0, h_&_m
2019-09-20;55.58, lidl
2019-09-21;50.0, withdrawal
2019-09-21;25.0, train_ticket"""


def get_categories():
    default_categories = [
        "misc",
        "uncategorized",
        ("food", [
            ("groceries", ["lidl", "aldi", "edeka", "rewe"]),
            "restaurant", "street_food"]),
        ("utilities", ["internet", "electricity", "cellphone_balance"]),
        ("travel", ["plane_ticket", "hotel_reservation", "train_ticket"]),
        ("tax", ["tv_tax"]),
        ("shopping", ["electronics", "clothing", "sports",
                      "home_goods", "furniture", "shopping_misc",
                      "shoes", "purses", "jewlery"]),
        ("education", [("course_fee", ["german_course"]),
                       "textbook", "school_supplies"]),
        ("body_and_hygiene", ["perfume", "hair_product",
                              "hairdresser", "nails"]),
        ("commuting", ["monthly_ticket",
                       "day_ticket", "single_ticket"])
    ]

    return categories.categories_from_list(default_categories)


def parse_date(dt):
    return datetime.strptime(dt, "%Y-%m-%d").date()


def records(cats):
    recs = (tuple(line.split(";")) for line in records_.split("\n"))
    return [
        (parse_date(date), parse_transaction(trans, cats))
        for date, trans in recs
    ]


def get_backend(categories, records):
    backend = MemoryBackend(categories)

    for date, rec in records:
        backend.insert_record(date, rec)

    return backend


cats = get_categories()

backend = get_backend(
    cats,
    records(cats)
)

app = Flask(__name__)
app.register_blueprint(transactions_blueprint(backend, __name__))
