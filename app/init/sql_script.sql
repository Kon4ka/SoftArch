CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_login VARCHAR(255) UNIQUE,
    user_name VARCHAR(255),
    user_surname VARCHAR(255),
    user_password VARCHAR(255)
);

CREATE INDEX user_id_index ON users (user_id);
CREATE INDEX user_login_index ON users (user_login);
CREATE INDEX user_name_index ON users (user_name);
CREATE INDEX user_surname_index ON users (user_surname);

-- CREATE TABLE reports (
--     report_id SERIAL PRIMARY KEY,
--     report_title VARCHAR(200) NOT NULL,
--     mongodb_id VARCHAR(100) UNIQUE NOT NULL
-- );

-- CREATE INDEX report_id_index ON reports (report_id);

-- CREATE TABLE conferences (
--     conference_id SERIAL PRIMARY KEY,
--     conference_name VARCHAR(300) NOT NULL,
--     conference_date INT NOT NULL,
--     conference_description TEXT
-- );

-- CREATE TABLE conferences_admins (
--     id SERIAL PRIMARY KEY,
--     conference_id INT REFERENCES conferences(conference_id),
--     user_id INT REFERENCES users(user_id),
--     UNIQUE (conference_id, user_id)
-- );

-- CREATE TABLE reports_users (
--     id SERIAL PRIMARY KEY,
--     report_id INT REFERENCES reports(report_id),
--     user_id INT REFERENCES users(user_id),
--     UNIQUE (report_id, user_id)
-- );

-- CREATE TABLE conferences_reports (
--     id SERIAL PRIMARY KEY,
--     conference_id INT REFERENCES conferences(conference_id),
--     report_id INT REFERENCES reports(report_id),
--     UNIQUE (conference_id, report_id)
-- );

-- CREATE INDEX conference_id_index ON conferences (conference_id);
-- CREATE INDEX conference_name_index ON conferences (conference_name);
-- CREATE INDEX conference_date_index ON conferences (conference_date);