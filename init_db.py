import sqlite3

connection = sqlite3.connect('database.db')

cur = connection.cursor()

cur.execute('DROP TABLE IF EXISTS articles;')
cur.execute('CREATE TABLE articles (id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'title varchar(100) NOT NULL,'
            'author varchar(100) NOT NULL,'
            'content text NOT NULL,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )

cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'nickname varchar(100) NOT NULL,'
            'email varchar(100) NOT NULL,'
            'password varchar(100) NOT NULL,'
            'date_reg date DEFAULT CURRENT_TIMESTAMP);'
            )

cur.execute('INSERT INTO articles (title, author, content)'
            'VALUES (?, ?, ?)',
            ('First test article',
             'Admin',
             'There is not content, im just checking the db.')
            )

connection.commit()
cur.close()
connection.close()
