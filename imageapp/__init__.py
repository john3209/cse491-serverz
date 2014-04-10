# __init__.py is the top level file in a Python package.

import create
import retrieve
from quixote.publish import Publisher
from .root import RootDirectory
from . import html, image
from PIL import Image

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup(): # Stuff that should be run once.
    html.init_templates()

    create.create_image_table() # Ensures image table exists.

    if retrieve.get_image_count() == 0:
        some_data = open('imageapp/dice.png', 'rb').read()
        image.add_image(some_data, 'png', 'Dice', 'Some dice!')
    
def teardown(): # Stuff that should be run once.
    pass
