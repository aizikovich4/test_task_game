DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS items;

CREATE TABLE IF NOT EXISTS users(
	id_user INTEGER PRIMARY KEY, 
	login TEXT NOT NULL, 
	credit INTEGER
);

CREATE TABLE IF NOT EXISTS items(
	id_item INTEGER PRIMARY KEY, 
	name TEXT NOT NULL, 
	price INTEGER
);

INSERT INTO users(login, credit) VALUES('1',100);
INSERT INTO users(login, credit) VALUES('2',200);
INSERT INTO users(login, credit) VALUES('qwe',300);
INSERT INTO users(login, credit) VALUES('qqq',123);

INSERT INTO items(name, price) VALUES('ship1',123);
INSERT INTO items(name, price) VALUES('ship2',444);
INSERT INTO items(name, price) VALUES('ship3',555);
INSERT INTO items(name, price) VALUES('weapon1',666);
INSERT INTO items(name, price) VALUES('weapon2',77);



CREATE TABLE user_items ( 
	user_id INTEGER, 
	item_id INTEGER, 
	FOREIGN KEY(user_id) REFERENCES users(id_user), 
	FOREIGN KEY(item_id) REFERENCES items(id_item) 
);