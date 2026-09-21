from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round


def create_spark_session():
    return (
        SparkSession.builder
        .appName("SupplyChainGoldDataset")
        .master("local[*]")
        .getOrCreate()
    )


def main():

    spark = create_spark_session()

    print("\nStarting Gold Dataset Pipeline...")

    # --------------------------------------------------
    # 1. Read cleaned datasets
    # --------------------------------------------------

    orders = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/processed/orders.csv")
    )

    inventory = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/processed/inventory.csv")
    )

    suppliers = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/processed/suppliers.csv")
    )

    print("\nOrders:", orders.count())
    print("Inventory:", inventory.count())
    print("Suppliers:", suppliers.count())

    # --------------------------------------------------
    # 2. Join orders with suppliers
    # --------------------------------------------------

    gold = orders.join(
        suppliers,
        on="supplier_id",
        how="left"
    )

    # --------------------------------------------------
    # 3. Join with inventory
    # --------------------------------------------------

    gold = gold.join(
        inventory,
        on="product_id",
        how="left"
    )

    # --------------------------------------------------
    # 4. Calculate total order value
    # --------------------------------------------------

    gold = gold.withColumn(
        "total_order_value",
        round(
            col("quantity") * col("unit_price"),
            2
        )
    )

    # --------------------------------------------------
    # 5. Select analytics-ready columns
    # --------------------------------------------------

    gold = gold.select(
        "order_id",
        "order_date",
        "product_id",
        "supplier_id",
        "supplier_name",
        "country",
        "delivery_days",
        "quality_rating",
        "quality_category",
        "quantity",
        "unit_price",
        "total_order_value",
        "status",
        "stock_quantity",
        "reorder_level",
        "stock_status"
    )

    # --------------------------------------------------
    # 6. Display Gold dataset
    # --------------------------------------------------

    print("\nGold Dataset:")
    gold.show(10, truncate=False)

    print("\nGold Schema:")
    gold.printSchema()

    print("\nGold record count:", gold.count())

    # --------------------------------------------------
    # 7. Save Gold dataset
    # --------------------------------------------------

    output_path = "data/processed/gold_supply_chain.csv"

    print("\nConverting Gold DataFrame to Pandas...")

    gold_pd = gold.toPandas()

    print("Pandas rows:", len(gold_pd))

    gold_pd.to_csv(
        output_path,
        index=False
    )

    print("\nGold dataset saved to:")
    print(output_path)

    spark.stop()


if __name__ == "__main__":
    main()