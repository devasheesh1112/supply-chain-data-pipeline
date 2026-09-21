import pandas as pd


DATA_PATH = "data"


def load_dataset(filename):
    file_path = f"{DATA_PATH}/{filename}"

    df = pd.read_csv(file_path)

    print(f"\nLoaded: {filename}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    return df


def profile_dataset(df, name):
    print(f"\n{'=' * 50}")
    print(f"DATASET: {name}")
    print(f"{'=' * 50}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nFirst 5 Records:")
    print(df.head())


def main():
    suppliers = load_dataset("suppliers.csv")
    inventory = load_dataset("inventory.csv")
    orders = load_dataset("orders.csv")

    profile_dataset(suppliers, "Suppliers")
    profile_dataset(inventory, "Inventory")
    profile_dataset(orders, "Orders")


if __name__ == "__main__":
    main()