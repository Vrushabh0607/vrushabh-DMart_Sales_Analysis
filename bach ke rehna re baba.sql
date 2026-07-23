create database banking; 
use banking;                                    
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
alter table accounts drop foreign key accounts_ibfk_1;
set foreign_key_checks=0;

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
(2,'Vrushabh','Dakwe',9012345678,'vrushabh@email.com',433.40,'2026-03-04'),
(3,'Deepak','Kadam',9012345675,'deepak@email.com',433.40,'2026-03-04'),
(4,'Aryan','Kashyap',9476345678,'aryan@email.com',433.40,'2026-03-04'),
(5,'Muaviz','Khan',9012316258,'muaviz@email.com',433.40,'2026-03-04');
desc customers;
select * from customers;
alter table customers modify column phone bigint unique;

insert into accounts (account_id,account_type,balance,customer_id)values
(11,'savings',45637.50,1),
(12,'current',23432.40,2),
(13,'savings',21242.40,3),
(14,'current',52432.40,4),
(15,'savings',72132.40,5);

select * from accounts;
drop table accounts;
#update

update customers set email='vrushabhdakwe@gmail.com' where first_name='Vrushabh';
update customers set salary=360.90 where customer_id=1;
set sql_safe_updates=0;

#delete 
delete from accounts where account_id=11;

#truncate 
truncate table accounts;
truncate table customers;

#DQL

select account_type,balance from accounts where customer_id=1;
select account_id,balance from accounts where account_type='savings';
select email,salary from customers where phone=1234567890;

select account_id,balance from accounts where balance>25000;
select max(balance) from accounts;
select balance from accounts order by balance;
select balance from accounts order by balance desc ;
select balance from accounts order by balance desc limit 1;
select balance from accounts order by balance desc limit 1 offset 1;
