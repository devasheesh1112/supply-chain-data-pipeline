-- =========================================================
-- Supply Chain Analytics
-- =========================================================

-- 1. Overall order performance
SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(total_order_value), 2) AS total_order_value,
    ROUND(AVG(total_order_value), 2) AS average_order_value
FROM gold_supply_chain;


-- 2. Orders by status
SELECT
    status,
    COUNT(*) AS order_count,
    ROUND(SUM(total_order_value), 2) AS total_order_value
FROM gold_supply_chain
GROUP BY status
ORDER BY order_count DESC;


-- 3. Inventory status
SELECT
    stock_status,
    COUNT(*) AS record_count
FROM gold_supply_chain
GROUP BY stock_status
ORDER BY record_count DESC;


-- 4. Supplier quality performance
SELECT
    quality_category,
    COUNT(*) AS order_count,
    ROUND(SUM(total_order_value), 2) AS total_order_value
FROM gold_supply_chain
GROUP BY quality_category
ORDER BY total_order_value DESC;


-- 5. Top 10 suppliers by order value
SELECT
    supplier_id,
    supplier_name,
    COUNT(*) AS order_count,
    ROUND(SUM(total_order_value), 2) AS total_order_value
FROM gold_supply_chain
GROUP BY supplier_id, supplier_name
ORDER BY total_order_value DESC
LIMIT 10;


-- 6. Top products by order value
SELECT
    product_id,
    COUNT(*) AS order_count,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(total_order_value), 2) AS total_order_value
FROM gold_supply_chain
GROUP BY product_id
ORDER BY total_order_value DESC
LIMIT 10;


-- 7. Country-level performance
SELECT
    country,
    COUNT(*) AS order_count,
    ROUND(SUM(total_order_value), 2) AS total_order_value,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days
FROM gold_supply_chain
GROUP BY country
ORDER BY total_order_value DESC;


-- 8. Low-stock products
SELECT DISTINCT
    product_id,
    stock_quantity,
    reorder_level,
    stock_status
FROM gold_supply_chain
WHERE stock_status = 'LOW_STOCK'
ORDER BY stock_quantity ASC;