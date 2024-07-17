CREATE TABLE IF NOT EXISTS mainmenu (
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id integer PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    email text NOT NULL,
    password_hash text NOT NULL,
    is_psychologist integer NOT NULL CHECK (is_psychologist IN (0, 1)),
    profile_image text NOT NULL,
    bio text NOT NULL,
    qualification text NOT NULL,
    experience text NOT NULL,
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL
);

CREATE TABLE IF NOT EXISTS appointments (
    appointment_id integer PRIMARY KEY AUTOINCREMENT,
    client_id integer NOT NULL,
    psychologist_id integer NOT NULL,
    appointment_date datetime NOT NULL,
    appointment_type text NOT NULL,
    status text NOT NULL,
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    FOREIGN KEY (client_id) REFERENCES users(user_id),
    FOREIGN KEY (psychologist_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id integer PRIMARY KEY AUTOINCREMENT,
    client_id integer NOT NULL,
    psychologist_id integer NOT NULL,
    rating integer NOT NULL,
    comment text NOT NULL,
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    FOREIGN KEY (client_id) REFERENCES users(user_id),
    FOREIGN KEY (psychologist_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS schedules (
    schedule_id integer PRIMARY KEY AUTOINCREMENT,
    psychologist_id integer NOT NULL,
    available_date datetime NOT NULL,
    is_booked integer NOT NULL,
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    FOREIGN KEY (psychologist_id) REFERENCES users(user_id)
);

-- Создание триггеров для проверки поля is_psychologist

-- Триггер для таблицы appointments
CREATE TRIGGER check_psychologist_in_appointments
BEFORE INSERT ON appointments
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT is_psychologist FROM users WHERE user_id = NEW.psychologist_id) != 1 THEN
            RAISE (ABORT, 'The psychologist_id must reference a user with is_psychologist = 1')
    END;
END;

-- Триггер для таблицы reviews
CREATE TRIGGER check_psychologist_in_reviews
BEFORE INSERT ON reviews
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT is_psychologist FROM users WHERE user_id = NEW.psychologist_id) != 1 THEN
            RAISE (ABORT, 'The psychologist_id must reference a user with is_psychologist = 1')
    END;
END;

-- Триггер для таблицы schedules
CREATE TRIGGER check_psychologist_in_schedules
BEFORE INSERT ON schedules
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT is_psychologist FROM users WHERE user_id = NEW.psychologist_id) != 1 THEN
            RAISE (ABORT, 'The psychologist_id must reference a user with is_psychologist = 1')
    END;
END;