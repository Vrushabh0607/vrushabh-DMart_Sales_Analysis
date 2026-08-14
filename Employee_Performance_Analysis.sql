CREATE DATABASE employee_performance_db;
USE employee_performance_db;

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL,
    location VARCHAR(50)
);

desc departments;

INSERT INTO departments
(department_id, department_name, location)
VALUES
(101, 'IT', 'Mumbai'),
(102, 'HR', 'Pune'),
(103, 'Finance', 'Mumbai'),
(104, 'Marketing', 'Bangalore'),
(105, 'Sales', 'Delhi');

SELECT * FROM departments;

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    age INT,
    department_id INT,
    joining_date DATE,
    salary DECIMAL(10,2),
    
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);

desc employees;

INSERT INTO employees
(employee_id, employee_name, gender, age, department_id, joining_date, salary)
VALUES
(1001, 'Aarav Sharma', 'Male', 25, 101, '2023-01-15', 55000),
(1002, 'Priya Patil', 'Female', 27, 102, '2024-03-10', 48000),
(1003, 'Rahul Mehta', 'Male', 30, 103, '2022-07-20', 72000),
(1004, 'Sneha Joshi', 'Female', 26, 104, '2025-01-12', 51000),
(1005, 'Aditya Shah', 'Male', 29, 105, '2023-11-05', 62000),
(1006, 'Neha Kulkarni', 'Female', 24, 101, '2025-02-18', 46000),
(1007, 'Rohan Desai', 'Male', 32, 103, '2021-06-25', 85000),
(1008, 'Ananya Singh', 'Female', 28, 104, '2024-09-14', 58000),
(1009, 'Karan Gupta', 'Male', 31, 105, '2022-04-11', 68000),
(1010, 'Isha Nair', 'Female', 23, 102, '2025-05-20', 44000),
(1011, 'Vivek Rao', 'Male', 35, 101, '2020-08-17', 92000),
(1012, 'Pooja Verma', 'Female', 29, 103, '2023-12-01', 70000),
(1013, 'Siddharth Jain', 'Male', 27, 104, '2025-06-10', 53000),
(1014, 'Meera Iyer', 'Female', 33, 105, '2021-09-22', 76000),
(1015, 'Arjun Kapoor', 'Male', 26, 101, '2024-01-08', 57000),
(1016, 'Riya Malhotra', 'Female', 30, 102, '2022-10-19', 61000),
(1017, 'Manish Yadav', 'Male', 38, 103, '2019-05-15', 98000),
(1018, 'Kavya Deshmukh', 'Female', 25, 104, '2025-08-01', 49000),
(1019, 'Nikhil Bansal', 'Male', 34, 105, '2023-06-13', 81000),
(1020, 'Simran Kaur', 'Female', 28, 101, '2025-09-05', 52000);

SELECT * FROM employees limit 5;

CREATE TABLE performance (
    performance_id INT PRIMARY KEY,
    employee_id INT,
    performance_rating DECIMAL(3,2),
    projects_completed INT,
    attendance_percentage DECIMAL(5,2),
    appraisal_year YEAR,
    
    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);

desc performance;

INSERT INTO performance
(performance_id, employee_id, performance_rating, projects_completed, attendance_percentage, appraisal_year)
VALUES
(1, 1001, 4.50, 8, 94.50, 2025),
(2, 1002, 4.20, 6, 91.00, 2025),
(3, 1003, 4.70, 10, 96.00, 2025),
(4, 1004, 3.90, 5, 88.50, 2025),
(5, 1005, 4.10, 7, 92.00, 2025),
(6, 1006, 3.80, 5, 89.00, 2025),
(7, 1007, 4.90, 12, 97.50, 2025),
(8, 1008, 4.30, 8, 93.00, 2025),
(9, 1009, 4.60, 9, 95.00, 2025),
(10, 1010, 3.70, 4, 87.50, 2025),
(11, 1011, 4.80, 11, 98.00, 2025),
(12, 1012, 4.40, 9, 94.00, 2025),
(13, 1013, 4.00, 6, 90.50, 2025),
(14, 1014, 4.50, 10, 96.00, 2025),
(15, 1015, 4.20, 7, 92.50, 2025),
(16, 1016, 3.90, 6, 89.50, 2025),
(17, 1017, 4.95, 13, 98.50, 2025),
(18, 1018, 3.80, 5, 91.50, 2025),
(19, 1019, 4.60, 10, 95.50, 2025),
(20, 1020, 4.30, 8, 93.50, 2025);

SELECT * FROM performance limit 5;

SELECT
    e.employee_id,
    e.employee_name,
    e.gender,
    e.age,
    d.department_name,
    e.joining_date,
    e.salary,
    p.performance_rating,
    p.projects_completed,
    p.attendance_percentage
FROM employees e
JOIN departments d
    ON e.department_id = d.department_id
JOIN performance p
    ON e.employee_id = p.employee_id;
    
    SELECT * FROM employees;
    
    SELECT
    e.employee_id,
    e.employee_name,
    e.gender,
    e.age,
    d.department_name,
    e.salary
FROM employees e
JOIN departments d
    ON e.department_id = d.department_id
WHERE d.department_name = 'IT';

SELECT COUNT(*) AS total_employees
FROM employees;

SELECT
    d.department_name AS Department,
    COUNT(e.employee_id) AS Employees
FROM departments d
JOIN employees e
    ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name;

SELECT
    d.department_name,
    COUNT(e.employee_id) AS total_employees
FROM departments d
JOIN employees e
    ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name;

SELECT
    ROUND(AVG(salary), 2) AS average_salary
FROM employees;

SELECT
    MAX(salary) AS highest_salary
FROM employees;

SELECT
    MIN(salary) AS lowest_salary
FROM employees;

SELECT
    ROUND(AVG(performance_rating), 2) AS average_performance_rating
FROM performance;

SELECT
    e.employee_id,
    e.employee_name,
    d.department_name,
    p.performance_rating
FROM employees e
JOIN departments d
    ON e.department_id = d.department_id
JOIN performance p
    ON e.employee_id = p.employee_id
ORDER BY p.performance_rating DESC
LIMIT 1;

SELECT
    e.employee_id,
    e.employee_name,
    d.department_name,
    p.performance_rating
FROM employees e
JOIN departments d
    ON e.department_id = d.department_id
JOIN performance p
    ON e.employee_id = p.employee_id
WHERE p.performance_rating > 4
ORDER BY p.performance_rating DESC;

SELECT
    e.employee_id,
    e.employee_name,
    d.department_name,
    p.attendance_percentage
FROM employees e
JOIN departments d
    ON e.department_id = d.department_id
JOIN performance p
    ON e.employee_id = p.employee_id
WHERE p.attendance_percentage > 90
ORDER BY p.attendance_percentage DESC;

SELECT
    SUM(projects_completed) AS total_projects_completed
FROM performance;

SELECT
    d.department_name,
    ROUND(AVG(p.performance_rating), 2) AS average_performance
FROM departments d
JOIN employees e
    ON d.department_id = e.department_id
JOIN performance p
    ON e.employee_id = p.employee_id
GROUP BY d.department_id, d.department_name
ORDER BY average_performance DESC;

SELECT
    d.department_name,
    ROUND(AVG(e.salary), 2) AS average_salary
FROM departments d
JOIN employees e
    ON d.department_id = e.department_id
GROUP BY d.department_id, d.department_name
ORDER BY average_salary DESC;

SELECT
    employee_id,
    employee_name,
    joining_date,
    salary
FROM employees
WHERE joining_date BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY joining_date;

-- youngest employee

SELECT
    employee_id,
    employee_name,
    age
FROM employees
ORDER BY age ASC
LIMIT 1;

-- oldest employee

SELECT
    employee_id,
    employee_name,
    age
FROM employees
ORDER BY age DESC
LIMIT 1;

SELECT
    gender,
    COUNT(*) AS total_employees
FROM employees
GROUP BY gender;

SELECT
    d.department_name,
    ROUND(AVG(p.performance_rating), 2) AS average_performance
FROM departments d
JOIN employees e
    ON d.department_id = e.department_id
JOIN performance p
    ON e.employee_id = p.employee_id
GROUP BY d.department_id, d.department_name
ORDER BY average_performance DESC
LIMIT 1;

SELECT
    e.employee_id,
    e.employee_name,
    d.department_name,
    p.performance_rating,
    p.projects_completed,
    p.attendance_percentage
FROM employees e
JOIN departments d
    ON e.department_id = d.department_id
JOIN performance p
    ON e.employee_id = p.employee_id
ORDER BY p.performance_rating DESC
LIMIT 5;
