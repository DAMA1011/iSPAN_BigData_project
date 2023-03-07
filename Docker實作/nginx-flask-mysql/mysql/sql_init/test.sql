create database test;

use test;

/*GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';*/

/*FLUSH PRIVILEGES;*/

CREATE TABLE restaurant(
google_url varchar(1900),
place_name varchar(300),
total_rating decimal(2,1),
total_reviews int,
address varchar(300),
phone varchar(50),
file_name_1 varchar(200),
new_district varchar(10),
monday varchar(1000),
tuesday varchar(1000),
wednesday varchar(1000),
thursday varchar(1000),
friday varchar(1000),
saturday varchar(1000),
sunday varchar(1000),
new_place_category varchar(30),
latitude decimal(20,10),
longitude decimal(20,10),
district_num int,
model_rating decimal(2,1)
);

LOAD DATA LOCAL INFILE "/data/restaurant_0114_final.csv"
INTO TABLE restaurant
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

CREATE TABLE spot(
google_url varchar(1900),
place_name varchar(300),
total_rating decimal(2,1),
total_reviews int,
address varchar(300),
phone varchar(50),
file_name_1 varchar(200),
new_district varchar(10),
monday varchar(1000),
tuesday varchar(1000),
wednesday varchar(1000),
thursday varchar(1000),
friday varchar(1000),
saturday varchar(1000),
sunday varchar(1000),
new_place_category varchar(30),
latitude decimal(20,10),
longitude decimal(20,10),
district_num int,
model_rating decimal(2,1)
);

LOAD DATA LOCAL INFILE "/data/spot_0114_final.csv"
INTO TABLE spot
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
