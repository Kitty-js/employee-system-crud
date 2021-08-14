CREATE DATABASE IF NOT EXISTS employee_database;

USE employee_database;

CREATE TABLE IF NOT EXISTS system(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    photo VARCHAR(5000) NOT NULL
);

-- Test
INSERT INTO system (name, email, photo) VALUES ('name1', 'name@name.com', 'photo.jpg');