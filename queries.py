
QUERIES = {
    'store_list': """
        SELECT * FROM store;
    """,
    'total_sales': """
        SELECT SUM(od.unitprice * od.quantity ) AS total_sales
        FROM order_details od
        JOIN orders o ON o.order_id = od.order_id
        WHERE o.OrderDate BETWEEN '2025-06-01' AND '2025-06-30';
    """,
    'employees_in_store': """
        SELECT e.name, e.role, s.name AS store_name
        FROM employee e
        LEFT JOIN store s ON e.store_id = s.store_id;
    """,
    'products_by_category': """
        SELECT c.name AS category, p.name AS product, p.price
        FROM product p
        JOIN category c ON p.category_id = c.category_id;
    """,
    'low_stock_products': """
        SELECT name, stock_level
        FROM product
        WHERE stock_level < 50;
    """,
    'orders_by_customer': """
        SELECT c.name, COUNT(o.order_id) AS order_count
        FROM customer c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name;
    """,
    'top_5_products': """
        SELECT p.name, SUM(od.quantity) AS total_quantity
        FROM product p
        JOIN order_details od ON p.product_id = od.product_id
        GROUP BY p.product_id, p.name
        ORDER BY total_quantity DESC
        LIMIT 5;
    """,
    'employees_salary': """
        SELECT name, salary
        FROM employee
        WHERE salary > 4000;
    """,
    'products_expiring_soon': """
        SELECT name, expiration_date
        FROM product
        WHERE expiration_date < DATE_ADD(CURDATE(), INTERVAL 30 DAY)
        AND expiration_date IS NOT NULL
        ORDER BY expiration_date;
    """,
    'orders_by_employee': """
        SELECT e.name, COUNT(o.order_id) AS order_count
        FROM employee e
        LEFT JOIN orders o ON e.employee_id = o.employee_id
        GROUP BY e.employee_id, e.name;
    """,
    'sales_by_store': """
        SELECT s.name AS store_name, SUM(od.unitprice * od.quantity ) AS total_sales
        FROM store s
        JOIN employee e ON s.store_id = e.store_id
        JOIN orders o ON e.employee_id = o.employee_id
        JOIN order_details od ON o.order_id = od.order_id
        WHERE o.OrderDate BETWEEN '2025-06-01' AND '2025-06-30'
        GROUP BY s.store_id, s.name;
    """,
    'top_customers': """
        SELECT c.name, SUM(od.unitprice * od.quantity ) AS total_spent
        FROM customer c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_details od ON o.order_id = od.order_id
        GROUP BY c.customer_id, c.name
        ORDER BY total_spent DESC
        LIMIT 5;
    """,
    'products_by_supplier': """
        SELECT s.name AS supplier, COUNT(p.product_id) AS product_count
        FROM supplier s
        LEFT JOIN product p ON s.supplier_id = p.supplier_id
        GROUP BY s.supplier_id, s.name;
    """,
    'average_order_value': """
        SELECT AVG(total) AS avg_order_value
        FROM (
            SELECT o.order_id, SUM(od.unitprice * od.quantity ) AS total
            FROM orders o
            JOIN order_details od ON o.order_id = od.order_id
            GROUP BY o.order_id
        ) AS order_totals;
    """,
    'warehouse_stock': """
        SELECT w.location, SUM(p.stock_level) AS total_stock
        FROM warehouse w
        LEFT JOIN product p ON w.warehouse_id = p.warehouse_id
        GROUP BY w.warehouse_id, w.location;
    """,
    'orders_per_day': """
        SELECT DATE(o.OrderDate) AS order_date, COUNT(o.order_id) AS order_count
        FROM orders o
        WHERE o.OrderDate BETWEEN '2025-06-01' AND '2025-06-30'
        GROUP BY DATE(o.OrderDate);
    """,
    'products_not_sold': """
        SELECT p.name
        FROM product p
        LEFT JOIN order_details od ON p.product_id = od.product_id
        WHERE od.product_id IS NULL;
    """,
    'employee_performance': """
        SELECT e.name, SUM(od.unitprice * od.quantity ) AS total_sales
        FROM employee e
        JOIN orders o ON e.employee_id = o.employee_id
        JOIN order_details od ON o.order_id = od.order_id
        WHERE o.OrderDate BETWEEN '2025-06-01' AND '2025-06-30'
        GROUP BY e.employee_id, e.name;
    """,
    'category_sales': """
        SELECT c.name AS category, SUM(od.unitprice * od.quantity ) AS total_sales
        FROM category c
        JOIN product p ON c.category_id = p.category_id
        JOIN order_details od ON p.product_id = od.product_id
        JOIN orders o ON od.order_id = o.order_id
        WHERE o.OrderDate BETWEEN '2025-06-01' AND '2025-06-30'
        GROUP BY c.category_id, c.name;
    """,
    'customer_order_frequency': """
        SELECT c.name, COUNT(o.order_id) AS order_count, MAX(o.OrderDate) AS last_order
        FROM customer c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name;
    """,
    'Detailed Order Analysis by Store, Employee, and Customer': """
        SELECT
            o.order_id,
            o.OrderDate,
            s.name AS store_name,
            e.name AS employee_name,
            c.name AS customer_name,
            GROUP_CONCAT(DISTINCT p.name SEPARATOR ', ') AS products_ordered,
            SUM(od.unitprice * od.quantity) AS total_order_value
        FROM orders o
        JOIN employee e ON o.employee_id = e.employee_id
        JOIN store s ON e.store_id = s.store_id
        JOIN customer c ON o.customer_id = c.customer_id
        JOIN order_details od ON o.order_id = od.order_id
        JOIN product p ON od.product_id = p.product_id
        GROUP BY o.order_id, o.OrderDate, s.name, e.name, c.name
        ORDER BY o.OrderDate DESC;  
    """,
    'Profit Analysis by Supplier, Category, Warehouse, and Store with Expiry Check': """
            SELECT
            s.name AS store_name,
            w.location AS warehouse_location,
            sup.name AS supplier_name,
            cat.name AS category_name,
            COUNT(DISTINCT o.order_id) AS orders_count,
            GROUP_CONCAT(DISTINCT p.name SEPARATOR ', ') AS products_sold,
            SUM(od.unitprice * od.quantity) AS total_revenue,
            COUNT(DISTINCT CASE WHEN p.expiration_date < CURDATE() THEN p.product_id END) AS expired_products
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN product p ON od.product_id = p.product_id
        JOIN category cat ON p.category_id = cat.category_id
        JOIN supplier sup ON p.supplier_id = sup.supplier_id
        JOIN employee e ON o.employee_id = e.employee_id
        JOIN store s ON e.store_id = s.store_id
        JOIN warehouse w ON p.warehouse_id = w.warehouse_id
        GROUP BY s.name, w.location, sup.name, cat.name
        ORDER BY total_revenue DESC;
        """
}