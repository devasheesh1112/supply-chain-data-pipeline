import pandas as pd


def check_orders(df):
    print("\n========== ORDERS QUALITY CHECK ==========")

    # Missing supplier IDs
    missing_supplier = df["supplier_id"].isna().sum()

    # Duplicate orders
    duplicate_orders = df["order_id"].duplicated().sum()

    # Invalid quantities
    invalid_quantity = (df["quantity"] <= 0).sum()

    # Invalid prices
    invalid_price = (df["unit_price"] <= 0).sum()

    print(f"Missing supplier_id : {missing_supplier}")
    print(f"Duplicate order_id  : {duplicate_orders}")
    print(f"Invalid quantity    : {invalid_quantity}")
    print(f"Invalid unit_price  : {invalid_price}")

    return {
        "missing_supplier": missing_supplier,
        "duplicate_orders": duplicate_orders,
        "invalid_quantity": invalid_quantity,
        "invalid_price": invalid_price,
    }


def check_inventory(df):
    print("\n========== INVENTORY QUALITY CHECK ==========")

    missing_stock = df["stock_quantity"].isna().sum()

    invalid_stock = (df["stock_quantity"] < 0).sum()

    invalid_reorder = (df["reorder_level"] < 0).sum()

    print(f"Missing stock_quantity : {missing_stock}")
    print(f"Invalid stock_quantity : {invalid_stock}")
    print(f"Invalid reorder_level  : {invalid_reorder}")

    return {
        "missing_stock": missing_stock,
        "invalid_stock": invalid_stock,
        "invalid_reorder": invalid_reorder,
    }


def check_suppliers(df):
    print("\n========== SUPPLIERS QUALITY CHECK ==========")

    duplicate_supplier = df["supplier_id"].duplicated().sum()

    invalid_delivery = (df["delivery_days"] < 0).sum()

    invalid_rating = (
        (df["quality_rating"] < 0)
        | (df["quality_rating"] > 5)
    ).sum()

    print(f"Duplicate supplier_id : {duplicate_supplier}")
    print(f"Invalid delivery_days : {invalid_delivery}")
    print(f"Invalid quality_rating: {invalid_rating}")

    return {
        "duplicate_supplier": duplicate_supplier,
        "invalid_delivery": invalid_delivery,
        "invalid_rating": invalid_rating,
    }


def main():

    orders = pd.read_csv("data/orders.csv")
    inventory = pd.read_csv("data/inventory.csv")
    suppliers = pd.read_csv("data/suppliers.csv")

    check_orders(orders)
    check_inventory(inventory)
    check_suppliers(suppliers)


if __name__ == "__main__":
    main()