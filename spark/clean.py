from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date


def create_spark_session():
    return (
        SparkSession.builder
        .appName("SupplyChainOrderCleaning")
        .master("local[*]")
        .config("spark.hadoop.fs.defaultFS", "file:///")
        .getOrCreate()
    )


def main():

    spark = create_spark_session()

    print("\nStarting Spark ETL...")

    # --------------------------------------------------
    # 1. Read raw orders
    # --------------------------------------------------

    orders = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/orders.csv")
    )

    print("\nRaw record count:", orders.count())

    # --------------------------------------------------
    # 2. Remove duplicate orders
    # --------------------------------------------------

    orders = orders.dropDuplicates(["order_id"])

    print("After removing duplicates:", orders.count())

    # --------------------------------------------------
    # 3. Remove records with missing supplier_id
    # --------------------------------------------------

    orders = orders.filter(
        col("supplier_id").isNotNull()
    )

    print("After removing missing suppliers:", orders.count())

    # --------------------------------------------------
    # 4. Remove invalid quantities
    # --------------------------------------------------

    orders = orders.filter(
        col("quantity") > 0
    )

    print("After removing invalid quantities:", orders.count())

    # --------------------------------------------------
    # 5. Convert order_date to proper DATE type
    # --------------------------------------------------

    orders = orders.withColumn(
        "order_date",
        to_date(col("order_date"), "yyyy-MM-dd")
    )

    # --------------------------------------------------
    # 6. Display cleaned data
    # --------------------------------------------------

    print("\nCleaned Orders:")
    orders.show(10, truncate=False)

    print("\nFinal Schema:")
    orders.printSchema()

    # --------------------------------------------------
    # 7. Save cleaned data

    output_path = "data/processed/orders"

    (
        orders.write
        .mode("overwrite")
        .option("header", True)
        .csv(output_path)
    )

    print("\nCleaned orders saved to:")
    print(output_path)



if __name__ == "__main__":
    main()