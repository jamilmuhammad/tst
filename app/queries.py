# SQL Queries
CREATE_TABLES_QUERY = """
CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    birth_date DATE
);

CREATE INDEX IF NOT EXISTS idx_authors_name ON authors(name);

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    publish_date DATE,
    author_id INTEGER REFERENCES authors(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_books_author_id ON books(author_id);
"""

# Author Queries
GET_AUTHORS = """
SELECT 
    a.id, 
    a.name, 
    a.bio, 
    a.birth_date,
    COALESCE(json_agg(
        json_build_object(
            'id', b.id,
            'title', b.title,
            'description', b.description,
            'publish_date', b.publish_date,
            'author_id', b.author_id
        ) 
        ORDER BY b.id
    ) FILTER (WHERE b.id IS NOT NULL), '[]') as books
FROM authors a
LEFT JOIN books b ON a.id = b.author_id
GROUP BY a.id
ORDER BY a.id
OFFSET %s LIMIT %s;
"""

GET_AUTHOR = """
SELECT 
    a.id, 
    a.name, 
    a.bio, 
    a.birth_date,
    COALESCE(json_agg(
        json_build_object(
            'id', b.id,
            'title', b.title,
            'description', b.description,
            'publish_date', b.publish_date,
            'author_id', b.author_id
        ) 
        ORDER BY b.id
    ) FILTER (WHERE b.id IS NOT NULL), '[]') as books
FROM authors a
LEFT JOIN books b ON a.id = b.author_id
WHERE a.id = %s
GROUP BY a.id;
"""

CREATE_AUTHOR = """
INSERT INTO authors (name, bio, birth_date)
VALUES (%s, %s, %s)
RETURNING id, name, bio, birth_date;
"""

UPDATE_AUTHOR = """
UPDATE authors 
SET name = %s, bio = %s, birth_date = %s
WHERE id = %s
RETURNING id, name, bio, birth_date;
"""

DELETE_AUTHOR = """
DELETE FROM authors
WHERE id = %s
RETURNING id, name, bio, birth_date;
"""

# Book Queries
GET_BOOKS = """
SELECT b.*, 
       json_build_object(
           'id', a.id,
           'name', a.name,
           'bio', a.bio,
           'birth_date', a.birth_date
       ) as author
FROM books b
JOIN authors a ON b.author_id = a.id
ORDER BY b.id
OFFSET %s LIMIT %s;
"""

GET_BOOK = """
SELECT b.*, 
       json_build_object(
           'id', a.id,
           'name', a.name,
           'bio', a.bio,
           'birth_date', a.birth_date
       ) as author
FROM books b
JOIN authors a ON b.author_id = a.id
WHERE b.id = %s;
"""

CREATE_BOOK = """
INSERT INTO books (title, description, publish_date, author_id)
VALUES (%s, %s, %s, %s)
RETURNING id, title, description, publish_date, author_id;
"""

UPDATE_BOOK = """
UPDATE books 
SET title = %s, description = %s, publish_date = %s, author_id = %s
WHERE id = %s
RETURNING id, title, description, publish_date, author_id;
"""

DELETE_BOOK = """
DELETE FROM books
WHERE id = %s
RETURNING id, title, description, publish_date, author_id;
"""

GET_AUTHOR_BOOKS = """
SELECT b.*, 
       json_build_object(
           'id', a.id,
           'name', a.name,
           'bio', a.bio,
           'birth_date', a.birth_date
       ) as author
FROM books b
JOIN authors a ON b.author_id = a.id
WHERE b.author_id = %s
ORDER BY b.id
OFFSET %s LIMIT %s;
"""