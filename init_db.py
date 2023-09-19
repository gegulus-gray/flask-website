import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Hula by Jasmin Iolani Hakes', 'Hula is not only one of the best beach read of 2023, but it’s also one of the best books of 2023! I picked up this book based on the cover and the thoughts of the hula dance competition, but instead of the fun read I was expecting, I got a coming-of-age story about a light-skinned Hawaiian who is trying to prove she belongs by learning to Hula.')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Trees of the Emerald Sea: A Cosmere Novel by Brandon Sanderon', 'If you love fantasy books of any kind, stop now and make time to read this fantastic book. This is the book that you would get if The Princess Bride had a book baby that empowered women everywhere to be the heroes in their own story, seek out adventure, and be brave enough to become who they were intended to be.')
            )

connection.commit()
connection.close()