import sqlite3
import sys

def get_latest_image():
    # Connect to database.
    db = sqlite3.connect('images.sqlite')

    # Configure to retrieve bytes, not text.
    db.text_factory = bytes

    # Get query handle and execute query.
    c = db.cursor()
    c.execute('SELECT image, imageType, name, descrip FROM image_store ORDER BY i DESC LIMIT 1')

    # Grab the first result (this will fail if no results!).
    image, imageType, name, descrip = c.fetchone()

    return (image, imageType, name, descrip)


def get_image(index):
    # Connect to database.
    db = sqlite3.connect('images.sqlite')

    # Configure to retrieve bytes, not text.
    db.text_factory = bytes

    # Get query handle and execute query.
    c = db.cursor()
    c.execute('SELECT image, imageType, name, descrip FROM (SELECT * FROM image_store ORDER BY i DESC LIMIT {0}) reverse ORDER BY i ASC'.format(index + 1))

    # Grab the first result (this will fail if no results!).
    image, imageType, name, descrip = c.fetchone()

    return (image, imageType, name, descrip)


def get_image_count():
    # Connect to database.
    db = sqlite3.connect('images.sqlite')

    # Get query handle and execute query.
    c = db.cursor()
    c.execute('SELECT COUNT(*) FROM image_store')

    # Grab the first result (this will fail if no results!).
    imageCount = c.fetchone()

    return imageCount[0]


def get_images(name, descrip):
    # Connect to database.
    db = sqlite3.connect('images.sqlite')

    # Get query handle and execute query.
    c = db.cursor()
    c.execute('SELECT i, name, descrip FROM image_store WHERE name LIKE \'%{0}%\' AND descrip LIKE \'%{1}%\''.format(name, descrip))

    return [dict(i=row[0],name=row[1],descrip=row[2]) for row in c.fetchall()]

def get_image_from_id(imageId):
    # Connect to database.
    db = sqlite3.connect('images.sqlite')

    # Configure to retrieve bytes, not text.
    db.text_factory = bytes

    # Get query handle and execute query.
    c = db.cursor()
    c.execute('SELECT image, imageType FROM image_store WHERE i={0}'.format(imageId))

    # Grab first result.
    image, imageType = c.fetchone()

    return (image, imageType)
