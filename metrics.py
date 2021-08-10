""" Calculate and print the values of 5 common accounting metrics:
Revenue, Expenses ,Gross Profit Margin, Net Profit Margin, Working Capital Ratio.
Assume all data from data.json are valid, so there is no need to validate it.
"""
import json
from decimal import Decimal

# To avoid typos when check field value
CATEGORY_REVENUE = "revenue"
CATEGORY_EXPENSE = "expense"
CATEGORY_ASSETS = "assets"
CATEGORY_LIABILITY = "liability"
VALUE_DEBIT = "debit"
VALUE_CREDIT = "credit"
TYPE_SALES = "sales"
TYPES_ASSETS = ("current", "bank", "current_accounts_receivable")
TYPES_LIABILITIES = ("current", "current_accounts_payable")


def get_values(transactions):
    """Returns revenue, expenses, profit, assets and liability."""
    values = {"revenue": 0, "expenses": 0, "profit": 0, "assets": 0, "liability": 0}
    for t in transactions:
        value = Decimal(t["total_value"])
        value_type = t["value_type"]
        category = t["account_category"]
        type = t["account_type"]

        # Total revenue
        if category == CATEGORY_REVENUE:
            values["revenue"] += value
        # Total expenses
        elif category == CATEGORY_EXPENSE:
            values["expenses"] += value
        # Total assets
        elif (
            category == CATEGORY_ASSETS
            and value_type == VALUE_DEBIT
            and type in TYPES_ASSETS
        ):
            values["assets"] += value
        elif (
            category == CATEGORY_ASSETS
            and value_type == VALUE_CREDIT
            and type in TYPES_ASSETS
        ):
            values["assets"] -= value
        # Total liability
        elif (
            category == CATEGORY_LIABILITY
            and value_type == VALUE_CREDIT
            and type in TYPES_LIABILITIES
        ):
            values["liability"] += value
        elif (
            category == CATEGORY_LIABILITY
            and value_type == VALUE_DEBIT
            and type in TYPES_LIABILITIES
        ):
            values["liability"] -= value

        # Gross profit
        if type == TYPE_SALES and value_type == VALUE_DEBIT:
            values["profit"] += value

    return values


def calculate_metrics(values):
    """Calculates profit and working capital ratio."""
    if values["revenue"] == 0:
        gross_profit_margin, net_profit_margin = 0, 0
    else:
        gross_profit_margin = round(values["profit"] / values["revenue"] * 100)
        net_profit_margin = round(
            (values["revenue"] - values["expenses"]) / values["revenue"] * 100
        )
    if values["liability"] == 0:
        working_capital_ratio = 0
    else:
        working_capital_ratio = round(values["assets"] / values["liability"] * 100)
    return {
        "gross_profit_margin": gross_profit_margin,
        "net_profit_margin": net_profit_margin,
        "working_capital_ratio": working_capital_ratio,
    }


def main(file):
    with open(file) as json_file:
        data = json.load(json_file).get("data")

    values = get_values(data)
    metrics = calculate_metrics(values)
    print(
        f"""Revenue: ${values["revenue"]:,.2f}
Expenses: ${values["expenses"]:,.2f}
Gross Profit Margin: {metrics["gross_profit_margin"]}%
Net Profit Margin: {metrics["net_profit_margin"]}%
Working Capital Ratio: {metrics["working_capital_ratio"]}%"""
    )


if __name__ == "__main__":
    main("data.json")
