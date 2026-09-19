import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker


fake = Faker()
random.seed(42)
Faker.seed(42)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

NUM_SUPPLIERS = 50
NUM_PRODUCTS = 500
NUM_ORDERS = 10_000

OUTPUT_DIR = "data"


# ---------------------------------------------------------
# 1. Generate Suppliers
# ---------------------------------------------------------

def generate_suppliers():
    suppliers = []

    countries = [
        "India",
        "USA",
        "Germany",
        "China",
        "Japan",
        "Mexico",
    ]

    for i in range(1, NUM_SUPPLIERS + 1):
        suppliers.append({
            "supplier_id": f"S{i:03d}",
            "supplier_name": fake.company(),
            "country": random.choice(countries),
            "delivery_days": random.randint(2, 30),
            "quality_rating": round(random.uniform(3.0, 5.0), 2),
        })

    return pd.DataFrame(suppliers)


# ---------------------------------------------------------
# 2. Generate Inventory
# ---------------------------------------------------------

def generate_inventory():
    inventory = []

    warehouses = ["WH01", "WH02", "WH03", "WH04", "WH05"]

    for i in range(1, NUM_PRODUCTS + 1):
        inventory.append({
            "product_id": f"P{i:04d}",
            "warehouse_id": random.choice(warehouses),
            "stock_quantity": random.randint(0, 5000),
            "reorder_level": random.randint(100, 1000),
            "last_updated": fake.date_between(
                start_date="-30d",
                end_date="today"
            ),
        })

    return pd.DataFrame(inventory)


# ---------------------------------------------------------
# 3. Generate Orders
# ---------------------------------------------------------

def generate_orders():
    orders = []

    start_date = datetime.now() - timedelta(days=180)

    statuses = [
        "Delivered",
        "Processing",
        "Shipped",
        "Cancelled",
    ]

    for i in range(1, NUM_ORDERS + 1):

        order_date = start_date + timedelta(
            days=random.randint(0, 180)
        )

        orders.append({
            "order_id": f"ORD{i:06d}",
            "product_id": f"P{random.randint(1, NUM_PRODUCTS):04d}",
            "supplier_id": f"S{random.randint(1, NUM_SUPPLIERS):03d}",
            "order_date": order_date.strftime("%Y-%m-%d"),
            "quantity": random.randint(1, 1000),
            "unit_price": round(random.uniform(10, 5000), 2),
            "status": random.choice(statuses),
        })

    return pd.DataFrame(orders)


# ---------------------------------------------------------
# 4. Introduce Data Quality Issues
# ---------------------------------------------------------

def introduce_data_quality_issues(orders, inventory):

    # Missing supplier IDs
    missing_indices = random.sample(
        range(len(orders)),
        20
    )

    orders.loc[missing_indices, "supplier_id"] = None


    # Invalid quantities
    invalid_indices = random.sample(
        range(len(orders)),
        10
    )

    orders.loc[invalid_indices, "quantity"] = -50


    # Duplicate orders
    duplicates = orders.sample(
        20,
        random_state=42
    )

    orders = pd.concat(
        [orders, duplicates],
        ignore_index=True
    )


    # Missing inventory quantities
    inventory_missing_indices = random.sample(
        range(len(inventory)),
        10
    )

    inventory.loc[
        inventory_missing_indices,
        "stock_quantity"
    ] = None

    return orders, inventory


# ---------------------------------------------------------
# 5. Main
# ---------------------------------------------------------

def main():

    print("Generating supply-chain datasets...")

    suppliers = generate_suppliers()
    inventory = generate_inventory()
    orders = generate_orders()

    orders, inventory = introduce_data_quality_issues(
        orders,
        inventory
    )

    suppliers.to_csv(
        f"{OUTPUT_DIR}/suppliers.csv",
        index=False
    )

    inventory.to_csv(
        f"{OUTPUT_DIR}/inventory.csv",
        index=False
    )

    orders.to_csv(
        f"{OUTPUT_DIR}/orders.csv",
        index=False
    )

    print("\nDatasets generated successfully!")

    print(f"Suppliers : {len(suppliers)}")
    print(f"Inventory : {len(inventory)}")
    print(f"Orders    : {len(orders)}")

    print("\nFiles created:")
    print("data/suppliers.csv")
    print("data/inventory.csv")
    print("data/orders.csv")


if __name__ == "__main__":
    main()