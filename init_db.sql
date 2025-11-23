CREATE DATABASE IF NOT EXISTS movie_info;
USE movie_info;

DROP TABLE IF EXISTS Movie;
DROP TABLE IF EXISTS Director;

CREATE TABLE Director (
    Person_ID INT PRIMARY KEY,
    Director_Name VARCHAR(50),
    Birth_Year INT,
    No_Of_Films INT,
    No_Of_Awards INT
);

CREATE TABLE Movie (
    Movie_ID INT PRIMARY KEY AUTO_INCREMENT,
    Movie_Name VARCHAR(100),
    Genre VARCHAR(30),
    Year INT,
    IMDb_Rating DECIMAL(3,1),
    Director_ID INT,
    FOREIGN KEY (Director_ID) REFERENCES Director(Person_ID)
);

INSERT INTO Director VALUES
(1, 'Zahir Raihan', 1935, 5, 5),
(2, 'Rajkumar Hirani', 1962, 5, 9),
(3, 'Satyajit Ray', 1921, 45, 55),
(4, 'Anjan Dutt', 1953, 23, 17),
(5, 'Rituparno Ghosh', 1963, 20, 15),
(6, 'Goutam Ghose', 1950, 12, 8),
(7, 'Aparna Sen', 1945, 12, 7),
(8, 'Kaushik Ganguly', 1968, 23, 30);

INSERT INTO Movie (Movie_Name, Genre, Year, IMDb_Rating, Director_ID) VALUES
('Pather Panchali', 'Drama', 1955, 8.5, 3),
('Noukadubi', 'Drama', 2011, 7.6, 5),
('Abohomaan', 'Drama', 2009, 7.3, 5),
('Joi Baba Felunath', 'Thriller', 1979, 8.0, 3),
('Jibon Theke Neya', 'Drama', 1970, 9.4, 1);
