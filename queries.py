# pylint: disable=missing-docstring, C0103
import sqlite3

conn = sqlite3.connect('data/movies.sqlite')
db = conn.cursor()

#db.execute("YOUR SQL QUERY")
#rows = db.fetchall()
#print(rows)
# => list (rows) of tuples (columns)

def directors_count(db):
    # return the number of directors contained in the database
    db.execute("select COUNT(id) from directors d ")
    rows = db.fetchone()
    return rows[0]  # return the integer instead of printing

def directors_list(db):
    # return the list of all the directors sorted in alphabetical order
    db.execute("select name from directors d order by name ASC;")
    rows = db.fetchall()
    director_names = [row[0] for row in rows]
    return director_names


def river_movies(db):
    # return the list of all movies which contain the exact word "river"
    # in their title, sorted in alphabetical order
    db.execute("""
               select title
from movies
WHERE title LIKE 'river'
           OR title LIKE 'river %'
           OR title LIKE '% river'
           OR title LIKE '% river %'
ORDER by title ASC;
""")
    rows = db.fetchall()
    return [row[0] for row in rows]

def directors_named_like_count(db, name):
    # return the number of directors which contain a given word in their name
    db.execute("SELECT COUNT(*) FROM directors WHERE name LIKE ?", ('%' + name + '%',))
    row = db.fetchone()
    return row[0]


def movies_longer_than(db, min_length):
    # return this list of all movies which are longer than a given duration,
    # sorted in the alphabetical order
    db.execute("SELECT title FROM movies WHERE minutes > ? ORDER BY title ASC;", (min_length,))
    rows = db.fetchall()
    return [row[0] for row in rows]

def main(word_arg, min_duration_arg):
    count = directors_named_like_count(db, word_arg)
    movies = movies_longer_than(db, min_duration_arg)

    return {
        "directors_count": count,
        "movies": movies
    }


if __name__ == "__main__":
    result = main("Fritz", 120)
    print("Number of directors containing 'Fritz':", result["directors_count"])
    print("Movies longer than 120:", result["movies"])
