CREATE TABLE orders (id serial primary key, order_number int4 NOT NULL, price_dollar real NOT NULL check (price_dollar>0), price_rur real NOT NULL check (price_rur>0), delivery_date date NOT NULL);
