"""
Import the MovieLens dataset into PostgreSQL
"""

import csv
import sqlalchemy
from secret import conn_str

movies = []  # list of lists
movie_genres = []  # list of lists
genre_set = set()


def to_int(s):
    try:
        return int(s)
    except:
        return None


with open('ml-latest-small/links.csv', 'rb') as f:
    reader = csv.reader(f)
    reader.next()  # skip header
    for row in reader:
        movie_id, imdb_id, tmdb_id = [to_int(_) for _ in row]
        movies.append([movie_id, imdb_id, tmdb_id])

with open('ml-latest-small/movies.csv', 'rb') as f:
    reader = csv.reader(f)
    reader.next()  # skip header
    i = 0
    for row in reader:
        _, title, genres = row
        try:
            year = int(title[-5:-1])
            title = title[:-7]
            movies[i].append(title)
            movies[i].append(year)
        except:
            movies[i].append(title)
            movies[i].append(None)

        genres = genres.split('|')
        movie_genres.append(genres)
        genre_set = genre_set.union(genres)

        i += 1

engine = sqlalchemy.create_engine(conn_str)
conn = engine.connect()

conn.execute('INSERT INTO movies VALUES (%s, %s, %s, %s, %s)', *movies)
conn.execute('INSERT INTO genres VALUES (%s)', *[(genre,) for genre in list(genre_set)])
multiparams = [(t[0][0], genre) for t in zip(movies, movie_genres) for genre in t[1]]
conn.execute('INSERT INTO movie_genres VALUES (%s, %s)', *multiparams)

conn.close()
