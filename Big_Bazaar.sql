show databases;
create database Big_Bazaar;
use Big_Bazaar;
show tables;

 create table customer(Customer_ID int(5) primary key,
					  Name char(25) not null,
                      Address varchar(255) not null,
                      Email_ID varchar(255),
                      Username varchar(30) not null unique,
                      Password varchar(30) not null unique);

create table Telephone_number(Phone_Number varchar(13) not null,
			                  Customer_ID int(5) not null, 
							  foreign key(Customer_ID) references customer(Customer_ID)ON UPDATE CASCADE
        ON DELETE CASCADE);
insert into Telephone_number values (9234567890,00001);
insert into Telephone_number values (9234852890,00001);
insert into Telephone_number values (9578954124,00002);
insert into Telephone_number values (7831516489,00002);
insert into Telephone_number values (8524567463,00003);
insert into Telephone_number values (8945637158,00003);
delete from Telephone_number;                              
create table Coupon_code(Coupon_name varchar(7) not null,
			             Customer_ID int(5) not null, 
                         foreign key(Customer_ID) references customer(Customer_ID) ON UPDATE CASCADE
        ON DELETE CASCADE);

create table Category(Category_ID int(3) primary key,
					  Category_name char(25) not null unique);
                      
create table Product(Product_ID int(5) primary key,
                     Item_name char(25) not null,
                     Item_info JSON not null,
                     Quantity int(3) not null,
                     Reviews JSON);

create table Cart(Customer_ID int(5) primary key,
				  Item_info JSON ,
                  Total_price float(12) not null); 		
use Big_Bazaar;
drop table _Order_;
drop table return_order;
drop table Order_history;
drop table Delivery;
drop table payment;
create table Payment(Payment_ID int(10) primary key,
					 Customer_ID int(5) not null,
					 Amount float(7) not null,
                     Payment_method varchar(10),
                     Coupon_code varchar(15));

create table _Order_(Order_ID int (5) primary key,
					 Payment_ID int(10) not null unique,
                     Customer_ID int(5) not null,
                     Amount char(20) not null,
                     Item_info JSON,
                     Order_Date date,
					 foreign key(Payment_ID) references Payment(Payment_ID) ON UPDATE CASCADE
        ON DELETE CASCADE);

create table Order_history(Order_ID int(5) primary key,
						   Customer_ID int(5) not null unique,
						   Payment_ID int(10) not null unique,
                           Order_Date DATE not null,
                           foreign key(Customer_ID) references customer(Customer_ID) ON UPDATE CASCADE
        ON DELETE CASCADE,
                           foreign key(Payment_ID) references Payment(Payment_ID)ON UPDATE CASCADE
        ON DELETE CASCADE);
                           
create table Return_order(Return_ID int(5) primary key,
                          Order_ID int(5) unique not null,
                          foreign key(Order_ID) references _Order_(Order_ID));
                          
insert into customer values (1,"Kriti","Punjabi Bagh","Kriti@gmail.com","kriti1","kritipunjabi");
insert into customer values (2,"Jai Kishan","Okhla 3","jaik@gmail.com","jk123@123","jaimatadi");
insert into customer values (3,"Raj Put","South ex","rajasthani@gmail.com","richboi","haveli100");                          
create table Supplier(Supplier_ID int(5) primary key,
					  Supplier_name char(25) not null,
					  Address varchar(255) not null,
                      Rating int(5) not null);
use big_bazaar;                      
delete from customer;
create table Delivery(Delivery_ID int(5) primary key, 
					  Customer_ID int(5) not null,
                      Order_ID int(5) not null unique,
                      Order_Status char(20) not null,
                      Helpline int(13) not null,
                      foreign key(Order_ID) references _Order_(Order_ID)ON UPDATE CASCADE ON DELETE CASCADE);
                      
insert into Category values (1,"Fruits & Vegetables");
insert into Category values (2,"Bakery");
insert into Category values (3,"Dairy");
insert into Category values (4,"Snacks");
insert into Category values (5,"Clothes");
insert into Category values (6,"Electronics");

insert into Product values (00001,"Capscicum",'{"Category_ID": "1", "Price": "120.45", "Availability": "Yes"}',500,null);
insert into Product values (00002,"Tomato",'{"Category_ID": "1", "Price": "045.00", "Availability": "Yes"}',600,null);
insert into Product values (00003,"Apple",'{"Category_ID": "1", "Price": "150.00", "Availability": "Yes"}',400,null);
insert into Product values (00004,"Onion",'{"Category_ID": "1", "Price": "25.00", "Availability": "Yes"}',800,null);
insert into Product values (00005,"Lemon",'{"Category_ID": "1", "Price": "250.00", "Availability": "Yes"}',300,null);

insert into Product values (00006,"Bread",'{"Category_ID": "2", "Price": "40", "Brand": "behemoth", "Availability": "Yes"}',400,null);
insert into Product values (00007,"Cupcake",'{"Category_ID": "2", "Price": "50", "Brand": "Brittania", "Availability": "Yes"}',500,null);
insert into Product values (00008,"Pao",'{"Category_ID": "2", "Price": "30", "Brand": "Harvest", "Availability": "Yes"}',300,null);

insert into Product values (00009,"Milk",'{"Category_ID": "3", "Price": "45", "Brand": "Amul", "Availability": "Yes"}',800,null);
insert into Product values (00010,"Butter",'{"Category_ID": "3", "Price": "50", "Brand": "Amul", "Availability": "Yes"}',500,null);
insert into Product values (00011,"Cheese",'{"Category_ID": "3", "Price": "90", "Brand": "Amul", "Availability": "Yes"}',400,null);

insert into Product values (00012,"Cream & Onion",'{"Category_ID": "4", "Price": "20", "Brand": "Lays", "Availability": "Yes"}',400,null);
insert into Product values (00013,"Namkeen",'{"Category_ID": "4", "Price": "30", "Brand": "Bhikaji", "Availability": "Yes"}',700,null);
insert into Product values (00014,"Dark Fantasy",'{"Category_ID": "4", "Price": "20", "Brand": "Sunfeast", "Availability": "Yes"}',300,null);

insert into Product values (00015,"Denim Jeans", '{"Category_ID": "5", "Price": "1399", "Brand": "Levis", "Availability": "Yes"}',100,null);
insert into Product values (00016,"T-shirt", '{"Category_ID": "5", "Price": "599", "Brand": "USPA", "Availability": "Yes"}',200,null);
insert into Product values (00017,"Shorts", '{"Category_ID": "5", "Price": "399", "Brand": "Puma", "Availability": "Yes"}',300,null);

insert into Product values (00018,"Ipad Air", '{"Category_ID": "6", "Price": "54999", "Brand": "Apple", "Availability": "Yes"}',20,null);
insert into Product values (00019,"Fitness tracker", '{"Category_ID": "6", "Price": "1999", "Brand": "Fitbit", "Availability": "Yes"}',250,null);
insert into Product values (00020,"Smartphone", '{"Category_ID": "6", "Price": "15999", "Brand": "Mi", "Availability": "Yes"}',100,null);

insert into Supplier values (00001,"Jaat Ram","Najafgarh",4);
insert into Supplier values (00002,"Gujjar mart","Noida",3);
insert into Supplier values (00003,"Narendra Yogi","Ghanta Ghar",1);

Select * from category;
Select * from product;
Select * from supplier;
