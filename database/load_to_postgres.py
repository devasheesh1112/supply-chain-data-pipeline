import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "supply_chain"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def load_suppliers(conn):
    df = pd.read_csv("data/processed/suppliers.csv")

    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO suppliers (
                supplier_id,
                supplier_name,
                country,
                delivery_days,
                quality_rating,
                quality_category
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (supplier_id) DO NOTHING;
            """,
            (
                row["supplier_id"],
                row["supplier_name"],
                row["country"],
                int(row["delivery_days"]),
                float(row["quality_rating"]),
                row["quality_category"],
            ),
        )

    conn.commit()
    cursor.close()

    print(f"Suppliers loaded: {len(df)}")


def load_inventory(conn):
    df = pd.read_csv("data/processed/inventory.csv")

    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO inventory (
                product_id,
                warehouse_id,
                stock_quantity,
                reorder_level,
                last_updated,
                stock_status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (product_id, warehouse_id) DO NOTHING;
            """,
            (
                row["product_id"],
                row["warehouse_id"],
                int(row["stock_quantity"]),
                int(row["reorder_level"]),
                row["last_updated"],
                row["stock_status"],
            ),
        )

    conn.commit()
    cursor.close()

    print(f"Inventory records loaded: {len(df)}")


def load_orders(conn):
    df = pd.read_csv("data/processed/orders.csv")

    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO orders (
                order_id,
                product_id,
                supplier_id,
                order_date,
                quantity,
                unit_price,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING;
            """,
            (
                row["order_id"],
                row["product_id"],
                row["supplier_id"],
                row["order_date"],
                int(row["quantity"]),
                float(row["unit_price"]),
                row["status"],
            ),
        )

    conn.commit()
    cursor.close()

    print(f"Orders loaded: {len(df)}")


def main():
    conn = get_connection()

    try:
        print("Connected to PostgreSQL")

        load_suppliers(conn)
        load_inventory(conn)
        load_orders(conn)

        print("All data loaded successfully.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()