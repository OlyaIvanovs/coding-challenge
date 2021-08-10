import metrics

import json
import pytest
from decimal import Decimal


@pytest.fixture(scope="module")
def test_data():
    with open("test.json") as json_file:
        data = json.load(json_file).get("data")
    return data


def test_calculating_revenue(test_data):
    values = metrics.get_values(test_data)
    assert values["revenue"] == Decimal("30000")


def test_calculating_expenses(test_data):
    values = metrics.get_values(test_data)
    assert values["expenses"] == Decimal("4500.50")


def test_calculating_gross_profit(test_data):
    values = metrics.get_values(test_data)
    assert values["profit"] == Decimal("20000")


def test_calculating_assets_if_only_credit(test_data):
    values = metrics.get_values(test_data)
    assert values["assets"] == Decimal("-500")


def test_calculating_liability(test_data):
    values = metrics.get_values(test_data)
    assert values["liability"] == Decimal("19000")


def test_calculating_metrics():
    values = {
        "revenue": Decimal("20000"),
        "expenses": Decimal("10000"),
        "profit": Decimal("490"),
        "assets": Decimal("2500"),
        "liability": Decimal("15000"),
    }
    res = metrics.calculate_metrics(values)
    assert res["gross_profit_margin"] == 2
    assert res["net_profit_margin"] == 50
    assert res["working_capital_ratio"] == 17


def test_calculating_metrics_if_revenue_0():
    values = {
        "revenue": Decimal("0"),
        "expenses": Decimal("10000"),
        "profit": Decimal("490"),
        "assets": Decimal("2500"),
        "liability": Decimal("15000"),
    }
    res = metrics.calculate_metrics(values)
    assert res["gross_profit_margin"] == 0
    assert res["net_profit_margin"] == 0


def test_calculating_working_ration_if_assets_0():
    values = {
        "revenue": Decimal("20000"),
        "expenses": Decimal("10000"),
        "profit": Decimal("490"),
        "assets": Decimal("0"),
        "liability": Decimal("15000"),
    }
    res = metrics.calculate_metrics(values)
    assert res["working_capital_ratio"] == 0
