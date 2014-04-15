import create
import insert
import retrieve

def add_image(data, imagetype, name, descrip):
    insert.insert_image(data, imagetype, name, descrip)

def get_image(num):
    return retrieve.get_image(num)

def get_latest_image():
    return retrieve.get_latest_image()

def get_image_count():
    return retrieve.get_image_count()
