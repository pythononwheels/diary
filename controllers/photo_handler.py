import os
from controllers.base_handler import BaseHandler
from models.photo import Photo
from models.user import User
from thumbnails import get_thumbnail
from PIL import Image
import glob, os

CARD_THUMBNAIL_WIDTH = 360
IMAGE_UPLOAD_DIR = "./static/images"
THUMBS_DIR = IMAGE_UPLOAD_DIR +"/tile_thumbs"

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

    def save_photos(self):
        """ creates a photo model and fills in the
            correct attribute values.
            the image itself is stored on the filesystem."""
        photo_list = []
        for file_list in self.request.files:
            # there is one list for each input file field. 
            # normally there should be only one. 
            for photo in self.request.files[file_list]:                
                # every phot represents a file_dict { "filename", "body", "content_type" }
                
                # prepare the filename and output path
                original_fname = photo['filename']
                extension = os.path.splitext(original_fname)[1]
                final_filename= os.path.normpath(os.path.join(IMAGE_UPLOAD_DIR,  original_fname))
                
                # create the photo model
                p = Photo()
                p.filename = original_fname
                p.file_extension = extension
                p.abspath = final_filename
                u=User(self.get_current_user())
                print("User: " + str(u.login) + " @id: " + str(u._id))
                print("User in db?: " + str(u.exists_in_db()))
                if not u.exists_in_db():
                    print(" ERROR : User not in DB")
                    self.redirect("/diary/error", msg="Der Benutzer " + str(self.get_current_user()) + "exisitert nicht.")
                output_file = open(final_filename, "wb")
                output_file.write(photo["body"])
                output_file.close()
                #p.type = imhdr.what(final_filename)
                #p.type = im.format
                p.user_id=u._id
                p.tags = self.get_argument("tags", [])
                p.title = self.get_argument("title", None)
                p.love_it = self.get_argument("love_it", False)
                # create the thumbnail for the cards
                p.thumbs[str(CARD_THUMBNAIL_WIDTH)] = self.create_thumbnail(
                        CARD_THUMBNAIL_WIDTH,
                        IMAGE_UPLOAD_DIR,
                        original_fname)
                # save photo model to DB
                p.upsert()
                photo_list.append(p)
        return photo_list


    def create_thumbnail(self, new_width, original_path, original_fname, opath=THUMBS_DIR):
        """ creates a thumbnail for the card view from the given
            image. With respect to the original image width:height ratio"""
        filename = os.path.splitext(original_fname)[0]
        extension = os.path.splitext(original_fname)[1]
        im = Image.open(os.path.join(original_path,original_fname))
        width = im.width
        height = im.height
        ratio = width / height
        new_height = new_width / ratio
        im.thumbnail((new_width,new_height))
        thumbfile_name = os.path.join(opath, filename + "_tile_thumb" + extension)
        im.save(thumbfile_name)
        return thumbfile_name

    def before_handler(self):
        self.default_methods["get"] = "new"
        self.default_methods["post"] = "new"

    def show_get(self):
        self.render("photo_show.tmpl", login=self.get_current_user())
    
    def new_get(self):
        self.render("photo_new_form.tmpl", login=self.get_current_user())

    def new_post(self):
        #self.print_file_info()
        photos = self.save_photos()
        print([str(photo.filename) for photo in photos])
        self.render("photo_show.tmpl", login=self.get_current_user())

    def cards_get(self):
        self.render("photo_cards.tmpl", photos=Photo.find_all(), login=self.get_current_user())

            