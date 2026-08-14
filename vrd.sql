create database db1;
use db1;
CREATE TABLE dim_state (
state_id INT PRIMARY KEY,
state_name VARCHAR(50)
);

CREATE TABLE dim_city (
city_id INT PRIMARY KEY,
city_name VARCHAR(50),
state_id INT,
FOREIGN KEY (state_id) REFERENCES dim_state(state_id)
);

CREATE TABLE dim_customer (
customer_id INT PRIMARY KEY,
customer_name VARCHAR(50),
city_id INT,
FOREIGN KEY (city_id) REFERENCES dim_city(city_id)
);

CREATE TABLE dim_category (
category_id INT PRIMARY KEY,
category_name VARCHAR(50)
);

CREATE TABLE dim_product (
product_id INT PRIMARY KEY,
product_name VARCHAR(50),
category_id INT,
FOREIGN KEY (category_id) REFERENCES dim_category(category_id)
);

CREATE TABLE fact_sales (
sales_id INT PRIMARY KEY,
customer_id INT,
product_id INT,
date_id INT,
sales_amount DECIMAL(10,2),

FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
FOREIGN KEY (product_id) REFERENCES dim_product(product_id));