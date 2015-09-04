import os
from controllers.base_handler import BaseHandler
from models.photo import Photo
from thumbnails import get_thumbnail
from PIL import Image
import glob, os


CARD_THUMBS = (360,180)
IMAGE_UPLOAD_DIR = "../static/images"

class PhotoHandler(BaseHandler):
    
    #
    # general RequestHandler docu see : http://tornado.readthedocs.org/en/latest/web.html
    #
    def initialize(self):
        """
            A dictionary passed as the third argument of a url spec will 
            be supplied as keyword arguments to initialize().

            Example:
            (r'/user/(.*)', ProfileHandler, dict(database=database)),
        """
        #self.database = database
        

    def print_file_info(self):
        #
        # print some info about the image uploads
        #
        print("files keys: " + str(self.request.files.keys())) 
        for file_list in self.request.files:
            print("len : " + str(file_list) + " : " + str(len(self.request.files[file_list])))
            for file_dict in self.request.files[file_list]:                
                print("file_dict keys: " + str(file_dict.keys()))
                for key in file_dict.keys():
                    if key not in ["body"]:
                        print(str(key) + " : " + str(file_dict[key]))

    def get_photos(self):
        for file_list in self.request.files:
            # there is one list for each input file field. 
            # normally there should be only one. 
            for photo in self.request.files[file_list]:                
                # every phot represents a file_dict { "filename", "body", "content_type" }
                original_fname = photo['filename']
                extension = os.path.splitext(original_fname)[1]
                final_filename= os.path.join(IMAGE_UPLOAD_DIR,  original_fname+extension)
                p = Photo()
                p.filename = original_fname
                p.file_extension = extension
                p.abspath = final_filename
                output_file = open(final_filename, "wb")
                output_file.write(photos["body"])
                output_file.close()
                p.to_db()


    def create_thumbnails(self):
        size = CARD_THUMBS
        
        infile = "test.png"
        file, ext = os.path.splitext(infile)
        im = Image.open(infile)
        print(dir(im))
        im.thumbnail(size)
        im.save(file + ".thumbnail.png")

    def before_handler(self):
        self.default_methods["get"] = "new"
        self.default_methods["post"] = "new"

    def new_get(self):
        self.render("photo_new_form.tmpl", login=self.get_current_user())

    def new_post(self):
        self.print_file_info()

        