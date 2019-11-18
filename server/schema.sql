DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users(
	id INTEGER PRIMARY KEY, 
	login TEXT NOT NULL, 
	credit INTEGER
);

INSERT INTO users(login, credit) VALUES('1',100);
INSERT INTO users(login, credit) VALUES('2',200);
INSERT INTO users(login, credit) VALUES('qwe',300);
INSERT INTO users(login, credit) VALUES('qqq',123);