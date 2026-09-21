from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when


def create_spark_session():
    return (
        SparkSession.builder
        .appName("SupplyChainInventoryCleaning")
        .master("local[*]")
        .getOrCreate()
    )


def main():

    spark = create_spark_session()

    print("\nStarting Inventory Spark ETL...")

    # --------------------------------------------------
    # 1. Read raw inventory
    # --------------------------------------------------

    inventory = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/inventory.csv")
    )

    print("\nRaw inventory records:", inventory.count())

    # --------------------------------------------------
    # 2. Check missing stock quantity
    # --------------------------------------------------

    print(
        "Missing stock_quantity:",
        inventory.filter(col("stock_quantity").isNull()).count()
    )

    # --------------------------------------------------
    # 3. Remove records with missing stock quantity
    # --------------------------------------------------

    inventory = inventory.filter(
        col("stock_quantity").isNotNull()
    )

    print(
        "After removing missing stock:",
        inventory.count()
    )

    # --------------------------------------------------
    # 4. Validate stock and reorder level
    # --------------------------------------------------

    inventory = inventory.filter(
        (col("stock_quantity") >= 0) &
        (col("reorder_level") >= 0)
    )

    print(
        "After validation:",
        inventory.count()
    )

    # --------------------------------------------------
    # 5. Create stock status
    # --------------------------------------------------

    inventory = inventory.withColumn(
        "stock_status",
        when(
            col("stock_quantity") < col("reorder_level"),
            "LOW_STOCK"
        ).otherwise("IN_STOCK")
    )

    # --------------------------------------------------
    # 6. Display cleaned inventory
    # --------------------------------------------------

    print("\nCleaned Inventory:")
    inventory.show(10, truncate=False)

    print("\nFinal Schema:")
    inventory.printSchema()

    # --------------------------------------------------
    # 7. Save cleaned inventory
    # --------------------------------------------------

    output_path = "data/processed/inventory.csv"

    print("\nConverting Spark DataFrame to Pandas...")

    cleaned_inventory = inventory.toPandas()

    print("Pandas rows:", len(cleaned_inventory))

    cleaned_inventory.to_csv(
        output_path,
        index=False
    )

    print("\nCleaned inventory saved to:")
    print(output_path)

    spark.stop()


if __name__ == "__main__":
    main()