""" Calculate and print the values of 5 common accounting metrics:
Revenue, Expenses ,Gross Profit Margin, Net Profit Margin, Working Capital Ratio.
Assume all data from data.json are valid, so there is no need to validate it.
"""
import json

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
        value = t["total_value"]
        value_type = t["value_type"]
        category = t["account_category"]
        type = t["account_type"]
        # Add up total revenue
        if category == CATEGORY_REVENUE:
            values["revenue"] += value
        # Add up total expenses
        elif category == CATEGORY_EXPENSE:
            values["expenses"] += value
        # Add up gross profit
        elif type == TYPE_SALES and value_type == VALUE_DEBIT:
            values["profit"] += value
        # Add up total assets
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
        # Add up total liability
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

    return values


def calculate_metrics(values):
    """Calculate metrics"""
    pass


if __name__ == "__main__":
    with open("data.json") as json_file:
        data = json.load(json_file).get("data")

    values = get_values(data)
    print(values)
    metrics = calculate_metrics(values)
