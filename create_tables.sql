drop  DATABASE SuperMarket;
create DATABASE SuperMarket;
USE SuperMarket;

CREATE TABLE store (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE warehouse (
    warehouse_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(255) NOT NULL
);

CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(255)
);

CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_level INT NOT NULL,
    expiration_date DATE,
    category_id INT NOT NULL,
    supplier_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(category_id) on update cascade,
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id) on update cascade,
    FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id)on update cascade
);

CREATE TABLE employee (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    salary DECIMAL(10,2),
    hire_date DATE,
    role VARCHAR(50) NOT NULL,
    store_id INT,
    warehouse_id INT,
    FOREIGN KEY (store_id) REFERENCES store(store_id) on update cascade,
    FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id) on update cascade
);

CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(100)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('customer', 'manager') NOT NULL,
    customer_id INT NULL,
    employee_id INT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) on update cascade ,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)on update cascade
);

CREATE TABLE orders(
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    employee_id INT NOT NULL,
    OrderDate DATE,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) on update cascade,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)on update cascade
);

CREATE TABLE order_details (
    product_id INT NOT NULL,
    order_id INT NOT NULL,
    unitprice DECIMAL(10,2) NOT NULL,
    Quantity INT default 1,
    PRIMARY KEY (product_id, order_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id) on update cascade,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)on update cascade on delete cascade
);


ALTER TABLE product AUTO_INCREMENT = 1;
SELECT * FROM store;
SELECT * FROM warehouse;
SELECT * FROM category;
SELECT * FROM supplier;
SELECT * FROM customer;
SELECT * FROM employee;
SELECT * FROM product;
SELECT * FROM users;
SELECT * FROM orders;
SELECT * FROM order_details;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE order_details;
TRUNCATE TABLE orders;
TRUNCATE TABLE users;
TRUNCATE TABLE product;
TRUNCATE TABLE employee;
TRUNCATE TABLE customer;
TRUNCATE TABLE supplier;
TRUNCATE TABLE category;
TRUNCATE TABLE warehouse;
TRUNCATE TABLE store;
SET FOREIGN_KEY_CHECKS = 1;


