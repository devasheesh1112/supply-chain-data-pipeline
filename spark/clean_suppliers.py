from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when


def create_spark_session():
    return (
        SparkSession.builder
        .appName("SupplyChainSupplierCleaning")
        .master("local[*]")
        .getOrCreate()
    )


def main():

    spark = create_spark_session()

    print("\nStarting Supplier Spark ETL...")

    # --------------------------------------------------
    # 1. Read raw suppliers
    # --------------------------------------------------

    suppliers = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/suppliers.csv")
    )

    print("\nRaw supplier records:", suppliers.count())

    # --------------------------------------------------
    # 2. Remove duplicate suppliers
    # --------------------------------------------------

    suppliers = suppliers.dropDuplicates(["supplier_id"])

    print(
        "After removing duplicate suppliers:",
        suppliers.count()
    )

    # --------------------------------------------------
    # 3. Validate supplier data
    # --------------------------------------------------

    suppliers = suppliers.filter(
        (col("delivery_days") >= 0) &
        (col("quality_rating") >= 0) &
        (col("quality_rating") <= 5)
    )

    print(
        "After validation:",
        suppliers.count()
    )

    # --------------------------------------------------
    # 4. Create supplier quality category
    # --------------------------------------------------

    suppliers = suppliers.withColumn(
        "quality_category",
        when(
            col("quality_rating") >= 4,
            "HIGH_QUALITY"
        ).otherwise("STANDARD")
    )

    # --------------------------------------------------
    # 5. Display cleaned suppliers
    # --------------------------------------------------

    print("\nCleaned Suppliers:")
    suppliers.show(10, truncate=False)

    print("\nFinal Schema:")
    suppliers.printSchema()

    # --------------------------------------------------
    # 6. Save cleaned suppliers
    # --------------------------------------------------

    output_path = "data/processed/suppliers.csv"

    print("\nConverting Spark DataFrame to Pandas...")

    cleaned_suppliers = suppliers.toPandas()

    print("Pandas rows:", len(cleaned_suppliers))

    cleaned_suppliers.to_csv(
        output_path,
        index=False
    )

    print("\nCleaned suppliers saved to:")
    print(output_path)

    spark.stop()


if __name__ == "__main__":
    main()