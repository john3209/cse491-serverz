import create
import insert
import retrieve

def add_image(data, imagetype, name, descrip):
    insert.insert_image(data, imagetype, name, descrip)

def add_comment(imageId, comment):
    insert.insert_comment(imageId, comment)

def image_exists(imageId):
    return retrieve.image_exists(imageId)

def get_latest_image_id():
    return retrieve.get_latest_image_id()

def get_image_count():
    return retrieve.get_image_count()

def get_images_by_metadata(name, descrip):
    return retrieve.get_images(name, descrip)

def get_image_by_id(imageId):
    return retrieve.get_image_from_id(imageId)

