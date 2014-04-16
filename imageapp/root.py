import os
import quixote
from quixote.directory import Directory, export, subdir
from PIL import Image
from io import BytesIO

from . import html, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='') # This makes it public.
    def index(self):
        img = image.get_latest_image()
        return html.render('index.html', {'name' : img[2], 'description' : img[3]})

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()
        the_file = request.form['file']
        name = request.form['name']
        descrip = request.form['description']

        # Gets image data.
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        # Gets image type.
        imagetype = the_file.orig_filename.rsplit('.', 1)[1].lower()
        if(imagetype in ['jpg', 'jpeg', 'jpe', 'jfif']):
            imagetype = 'jpeg'
        elif(imagetype in ['tif', 'tiff']):
            imagetype = 'tiff'
        else:
            imagetype = 'png'

        image.add_image(data, imagetype, name, descrip)

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        img = image.get_latest_image()
        return html.render('image.html', {'name' : img[2], 'description' : img[3]})

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()
        index = request.form['special']

        # If latest image, then no need for thumbnail.
        if(index == 'latest'):
            img = image.get_latest_image()
            response.set_content_type('image/{0}'.format(img[1]))
            return img[0]
        # Otherwise must be list of thumbnail images.
        else:
            img = image.get_image(int(index))
            response.set_content_type('image/{0}'.format(img[1]))

            # Temporary file used for Pillow.
            tmpFilePath = 'Temp.{0}'.format(img[1])

            # Create temp image.
            tmp = open(tmpFilePath, 'wb')
            tmp.write(img[0])
            tmp.close()

            # Make temp image a thumbnail.
            pilImg = Image.open(tmpFilePath)
            pilImg.thumbnail((250,250))
            pilImg.save(tmpFilePath)

            # Open temp image again to get image data.
            tmp = open(tmpFilePath, 'rb')
            data = tmp.read()
            tmp.close()

            # Remove temp image since we have data now.
            os.remove(tmpFilePath)
            return data


    @export(name='image_list')
    def image_list(self):
        return html.render('image_list.html', {'imageCount' : image.get_image_count()})

    @export(name='image_search')
    def image_search(self):
        return html.render('image_search.html')

    @export(name='image_results')
    def image_results(self):
        request = quixote.get_request()
        name = request.form['name']
        descrip = request.form['description']

        return html.render('image_results.html', {'images' : image.get_images_by_metadata(name, descrip)})

    @export(name='image_raw_id')
    def image_raw_id(self):
        response = quixote.get_response()
        request = quixote.get_request()
        imageId = request.form['id']

        img = image.get_image_by_id(imageId)
        response.set_content_type('image/{0}'.format(img[1]))
        return img[0]
