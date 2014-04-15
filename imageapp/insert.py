import sqlite3
import re

def insert_image(data, imageType, name, descrip):
    # Connects to the already existing database.
    db = sqlite3.connect('images.sqlite')

    # Configure to allow binary insertions.
    db.text_factory = bytes

    # Insert!
    db.execute("INSERT INTO image_store (image,imageType,name,descrip) VALUES (?,?,?,?)",(data,imageType,name,descrip,))
    db.commit()
    db.close()
