PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('418f2c6fc6ff');
CREATE TABLE users (
	id INTEGER NOT NULL, 
	email VARCHAR(50) NOT NULL, 
	password VARCHAR(100) NOT NULL, 
	is_superuser BOOLEAN NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	joined_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO users VALUES(1,'superuser@email.com','$2b$12$G4oxxrWClFskfdGwhYp.TeiJ/qWFqRObQfCerevQ2MltBfXnai/hm',1,1,'2024-07-26 15:29:08');
CREATE TABLE tokens (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	token VARCHAR(40) NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	UNIQUE (token)
);
CREATE TABLE ads (
	id VARCHAR(20) NOT NULL, 
	header VARCHAR(250) NOT NULL, 
	address VARCHAR(250), 
	author VARCHAR(50), 
	author_link VARCHAR(150), 
	views_count INTEGER NOT NULL, 
	position INTEGER NOT NULL, 
	is_archived BOOLEAN NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO ads VALUES('103295865','DEMO: Ремонт/Настройка видеонаблюдения: камер, регистраторов, домофонов. И т. д','Владивосток, улица Светланская 103, проспект 100-летия Владивостока 1, улица Морская 1-я 1/2, Выезд по городу и за город!!!',NULL,NULL,329,0,1,'2024-07-28 11:48:17');
INSERT INTO ads VALUES('97431275','DEMO: Монтаж видеонаблюдения Hikvision HiWatch Trassir, СКУД, домофонов','проспект Партизанский 26','doneit','https://www.farpost.ru/user/doneit/',527,1,0,'2024-07-28 12:11:13');
INSERT INTO ads VALUES('68025015','DEMO: Видеонаблюдение Установка Продажа Настройка Видеокамер IP','улица Шевченко 24 стр. 3, этаж 2','TVi MART','https://www.farpost.ru/user/TViMART/',1478,2,0,'2024-07-28 12:11:13');
INSERT INTO ads VALUES('116669935','DEMO: ВидеоКИТ - Системы видеонаблюдения, установка, обслуживание','остановка Покровский парк','VideoKIT','https://www.farpost.ru/user/VideoKIT/',185,3,0,'2024-07-28 12:11:13');
INSERT INTO ads VALUES('107283225','DEMO: Установка видеонаблюдения от Vladrec | Монтаж | Обслуживание | СКУД','проспект Народный 11в','VLADREC','https://www.farpost.ru/user/VLADREC2/',198,4,0,'2024-07-28 12:11:13');
INSERT INTO ads VALUES('119302225','DEMO: Установка видеонаблюдения. Монтаж Частный мастер.','','AndreyVideo2016','https://www.farpost.ru/user/AndreyVideo2016/',111,5,0,'2024-07-28 12:11:13');
INSERT INTO ads VALUES('45166575','DEMO: Продажа и установка видеонаблюдения. Монтаж любой сложности! Гарантия','г. Владивосток','Точка-Видео','https://www.farpost.ru/company/TochkaVideo/',3903,6,0,'2024-07-28 12:11:13');
INSERT INTO ads VALUES('78581325','DEMO: Монтаж-установка систем Видеонаблюдения от 1000 руб. Гарантия 3 года','улица Верхнепортовая 44','Точка-Видео','https://www.farpost.ru/company/TochkaVideo/',1099,7,0,'2024-07-28 12:11:13');
INSERT INTO ads VALUES('114559795','DEMO: Установка, видеонаблюдения видео/aуд домофоны, (обслуживание), СКУД, ОПС','улица Светланская 147, г. Владивосток, Артем, Пригород','AHDTechno','https://www.farpost.ru/user/AHDTechno/',383,8,0,'2024-07-28 12:11:13');
INSERT INTO ads VALUES('71222785','DEMO: Установка настройка монтаж , продажа видеонаблюдения и камер','торговый центр Строитель, улица Бородинская 46/50','Teleantennadv','https://www.farpost.ru/user/Teleantennadv/',2045,9,0,'2024-07-28 12:11:13');
INSERT INTO ads VALUES('109120705','DEMO: Пультовая охрана Монтаж охранно-пожарных систем видеонаблюдение СКУД','проспект 100-летия Владивостока 108','ООО ХОЛДИНГ БЕЗОПАСНОСТИ "АЭЛИТА-СЕКЬЮРИТИ"','https://www.farpost.ru/user/Aelita3/',496,10,0,'2024-07-28 12:11:13');
CREATE INDEX ix_users_id ON users (id);
CREATE INDEX ix_tokens_id ON tokens (id);
CREATE INDEX ix_ads_id ON ads (id);
COMMIT;
