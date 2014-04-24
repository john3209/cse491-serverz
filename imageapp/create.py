import sqlite3

def create_tables():
    # Ensures database is created by simply connecting to it.
    db = sqlite3.connect('images.sqlite')

    # Ensures image_store table exists. If already exists, does nothing.
    db.execute('CREATE TABLE IF NOT EXISTS image_store (i INTEGER PRIMARY KEY, image BLOB, imageType TEXT, name TEXT, descrip TEXT)');

    # Ensures image_store table exists. If already exists, does nothing.
    db.execute('CREATE TABLE IF NOT EXISTS image_comment (imageId INTEGER, comment TEXT)');

    # Commits transaction and closes connection.
    db.commit()
    db.close()
