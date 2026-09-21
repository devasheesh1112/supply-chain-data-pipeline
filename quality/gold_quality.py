import pandas as pd


def main():

    file_path = "data/processed/gold_supply_chain.csv"

    df = pd.read_csv(file_path)

    print("\n========== GOLD DATA QUALITY ==========")

    print("Total records:", len(df))

    # Missing values
    print("\nMissing values:")
    print(df.isnull().sum())

    # Duplicate orders
    print(
        "\nDuplicate order_id:",
        df["order_id"].duplicated().sum()
    )

    # Invalid quantities
    print(
        "Invalid quantity:",
        (df["quantity"] <= 0).sum()
    )

    # Invalid prices
    print(
        "Invalid unit_price:",
        (df["unit_price"] <= 0).sum()
    )

    # Invalid order values
    print(
        "Invalid total_order_value:",
        (df["total_order_value"] <= 0).sum()
    )

    # Missing supplier information
    print(
        "Missing supplier_name:",
        df["supplier_name"].isnull().sum()
    )

    # Missing inventory information
    print(
        "Missing stock_quantity:",
        df["stock_quantity"].isnull().sum()
    )

    # Business summary
    print("\n========== BUSINESS SUMMARY ==========")

    print(
        "Total order value:",
        round(df["total_order_value"].sum(), 2)
    )

    print("\nOrder status:")
    print(df["status"].value_counts())

    print("\nStock status:")
    print(df["stock_status"].value_counts())

    print("\nSupplier quality:")
    print(df["quality_category"].value_counts())


if __name__ == "__main__":
    main()