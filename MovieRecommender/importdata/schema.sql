DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS movie_genres;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  username TEXT PRIMARY KEY,
  password TEXT,
  CHECK (username SIMILAR TO '[a-zA-Z0-9_]+' AND username NOT LIKE 'movielens_%')
);

CREATE TABLE movies (
  movie_id INT PRIMARY KEY,
  imdb_id  INT,
  tmdb_id  INT,
  title    TEXT,
  year     INT
);

CREATE TABLE genres (
  genre TEXT PRIMARY KEY
);

CREATE TABLE movie_genres (
  movie_id INT REFERENCES movies,
  genre    TEXT REFERENCES genres
);

CREATE TABLE ratings (
  username TEXT REFERENCES users,
  movie_id INT REFERENCES movies,
  rating   REAL
);