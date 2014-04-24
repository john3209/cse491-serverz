import sqlite3
import sys

def image_exists(imageId):
    # Connect to database.
    db = sqlite3.connect('images.sqlite')

    # Get query handle and execute query.
    c = db.cursor()
    c.execute('SELECT i FROM image_store WHERE i={0}'.format(imageId))

    # Determines if there are any rows.
    if(c.fetchone()):
        return True
    else:
        return False

def get_latest_image_id():
    # Connect to database.
    db = sqlite3.connect('images.sqlite')

    # Get query handle and execute query.
    c = db.cursor()
    c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')

    # Grab the first result (this will fail if no results!).
    i = c.fetchone()[0]

    return i

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
    c.execute('SELECT i, image, imageType, name, descrip FROM image_store WHERE i={0}'.format(imageId))

    # Grab first result.
    i, image, imageType, name, descrip = c.fetchone()

    # Get comments for the image.
    c.execute('SELECT comment FROM image_comment WHERE imageId = {0}'.format(i))
    comments = [row[0] for row in c.fetchall()]

    return (image, imageType, name, descrip, comments, i)
