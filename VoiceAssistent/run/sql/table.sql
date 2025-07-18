CREATE TABLE IF NOT EXISTS people_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    lastname TEXT,
    patronymic TEXT,
    birthday DATE,
    role TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    telegram TEXT,
    vk TEXT,
    mom TEXT,
    passport TEXT,
    grandmother TEXT,
    grandfather TEXT,
    brother TEXT DEFAULT NULL,
    sister TEXT DEFAULT NULL,
    date_added DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS site (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    login TEXT NOT NULL,
    pasword TEXT NOT NULL,
    additional_information TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT NOT NULL,
    date_added DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_media_service TEXT NOT NULL,
    url TEXT NOT NULL,
    subscribes INTEGER NOT NULL,
    date_added DATE NOT NULL
);

-- CREATE TABLE IF NOT EXISTS my_database (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     type TEXT NOT NULL,
--     login TEXT NOT NULL,
--     pasword
--
-- )