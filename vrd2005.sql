show databases;
create database bankingdb;
use bankingdb;

create table customers (customer_id int auto_increment primary key,
first_name varchar(50) not null,
last_name varchar(50) not null,
phone bigint unique,
email varchar(50) not null,
occupation varchar(50),
salary decimal(5,2));
drop table customers;
desc customers;

show create table customers;
show create table accounts;

#Alter 
alter table customers add column creation_date date not null;
alter table customers drop column occupation;
SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE accounts DROP FOREIGN KEY accounts_ibfk_1;

SET FOREIGN_KEY_CHECKS = 1;

create table accounts(account_id int,
account_type varchar(50),
balance decimal(7,2),
customer_id int,foreign key(customer_id) references customers(customer_id));

alter table accounts add constraint fk_accounts foreign key (customer_id) references customers(customer_id);
desc customers;
desc accounts;

alter table customers modify column salary decimal(5,2);

#DML
insert into customers(customer_id,first_name,last_name,phone,email,salary,creation_date) values
(1,'Saurabh','Patil',1234567890,'saurabh@email.com',454.90,'2026-06-03'),
(2,'Vrushabh','Dakwe',9012345678,'vrushabh@email.com',412.40,'2026-03-04');
insert into customers(customer_id,first_name,last_name,phone,email,salary,creation_date) values
(3,'Deepak','Kadam',9012345675,'deepak@email.com',233.40,'2026-06-14'),
(4,'Aryan','Kashyap',9476345678,'aryan@email.com',973.40,'2026-11-24'),
(5,'Muaviz','Khan',9012316258,'muaviz@email.com',423.40,'2026-12-30');

insert into accounts(account_id,account_type,balance,customer_id) values
(11,'Savings',28745.67,1),
(12,'Current',28735.67,2),
(13,'Current',24595.67,3),
(14,'Savings',75675.67,4),
(15,'Current',83525.67,5);

select account_id,balance from accounts where account_type='Savings';
select email,salary from customers where phone=1234567890;

#order by
select account_id,balance from accounts where balance>25000;
select max(balance) from accounts;
select account_type,balance from accounts order by balance;
select balance from accounts order by balance desc ;
select balance from accounts order by balance desc limit 1;
select balance from accounts order by balance desc limit 3 offset 2;

#group by
select max(balance),account_type from accounts group by account_type;
select account_type from accounts group by account_type;
select distinct account_type from accounts;

#where clause
select * from customers;
select first_name from customers where first_name like 'v%';
select first_name,email from customers where first_name like '%z';
select first_name,email from customers where first_name like '%sha%';
select last_name,email,phone from customers where last_name like '__k%'; #letter k at third position in last name
select last_name,email,phone from customers where last_name like '_a%'; #letter a at second position in last name

#logical operators
select customer_id,first_name from customers where salary > 370;
select customer_id,first_name from customers where salary > 350 and creation_date>'2026-03-04';
select customer_id,first_name from customers where salary > 350 or creation_date>'2026-03-04';
select account_type,account_id from accounts where account_type !='savings'and balance>1000;

select account_id,balance,customer_id from accounts where account_type in ('savings','current');

SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    a.account_id,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a
ON c.customer_id = a.customer_id;

SELECT
    c.first_name,
    c.last_name,
    c.phone,
    c.email,
    c.salary,
    a.account_type,
    a.balance
FROM customers c
JOIN accounts a
ON c.customer_id = a.customer_id;

SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    a.balance
FROM customers c
JOIN accounts a
ON c.customer_id = a.customer_id
WHERE a.balance > 50000;

SELECT
    c.first_name,
    c.last_name,
    a.account_id,
    a.balance
FROM customers c
JOIN accounts a
ON c.customer_id = a.customer_id
WHERE a.account_type = 'Savings';

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    a.account_id,
    a.account_type,
    a.balance
FROM customers c
LEFT JOIN accounts a
ON c.customer_id = a.customer_id;

SELECT
    c.customer_id,
    c.first_name,
    c.last_name
FROM customers c
LEFT JOIN accounts a
ON c.customer_id = a.customer_id
WHERE a.account_id IS NULL;

SELECT
    c.first_name,
    c.last_name,
    a.account_id,
    a.account_type,
    a.balance
FROM customers c
RIGHT JOIN accounts a
ON c.customer_id = a.customer_id;

SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    a.balance
FROM customers c
JOIN accounts a
ON c.customer_id = a.customer_id
ORDER BY a.balance DESC;

CREATE VIEW customer_accounts AS
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    a.account_id,
    a.account_type,
    a.balance
FROM customers c
JOIN accounts a
ON c.customer_id = a.customer_id;

select * from customer_accounts;

CREATE INDEX idx_customer_firstname
ON customers(first_name);

CREATE INDEX idx_customer_email
ON customers(email);

SELECT *
FROM customers
WHERE email = 'vrushabh@email.com';


CREATE INDEX idx_account_type
ON accounts(account_type);

SELECT *
FROM accounts
WHERE account_type = 'Savings';