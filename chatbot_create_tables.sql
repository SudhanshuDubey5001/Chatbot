use Chatbot;

create table food_items(
  id INT AUTO_INCREMENT PRIMARY KEY,
  item VARCHAR(50) NOT NULL,
  price DECIMAL(6,2) NOT NULL
);

insert into food_items (item,price)
values 
	('Cheeseburger', 80),
	('French fries', 50),
	('Chicken nuggets', 90),
	('Pepperoni pizza', 120),
	('Hot dog', 70),
	('Fried chicken sandwich', 100),
	('Taco', 60),
	('Mozzarella sticks', 80),
	('Onion rings', 40),
	('Milkshake', 75);
    
select * from food_items;

create table order_details(
	order_id int not null,
    item_id int not null,
    quantity int not null,
    amount decimal not null,
    constraint fk_item_id
    foreign key (item_id) references food_items(id)
);

insert into order_details(order_id,item_id,quantity,amount)
values 
	(20, 1, 2, 160),
    (20, 3, 3, 270),
    (20, 10, 1, 75),
    (24, 7, 3, 180),
    (24, 9, 2, 80);
    
select * from order_details;

create table track_order(
	order_id int not null primary key,
    order_status varchar(30) not null
);

insert into track_order
values 
	(20, 'delivered'),
    (24, 'in-transit');
    
select * from track_order;
