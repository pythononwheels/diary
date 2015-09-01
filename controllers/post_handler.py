from controllers.base_handler import BaseHandler
from models.post import Post
import os
import tornado.web


IMAGE_UPLOAD_DIR = "../static/images"

class PostHandler(BaseHandler):
    """
        general RequestHandler docu see : http://tornado.readthedocs.org/en/latest/web.html
    """
    
    def initialize(self):
        """
            A dictionary passed as the third argument of a url spec will 
            be supplied as keyword arguments to initialize().

            Example:
            (r'/user/(.*)', ProfileHandler, dict(database=database)),
        """
        #self.database = database
        self.path = ""
        self.method = ""

    def new_get(self):
        """ render the create new post form """
        #self.print_debug_info()
        #self.render("post_new_form_test_bs_fileinput.tmpl", login=self.get_secure_cookie("login"))
        self.render("post_new_form_upload.tmpl", login=self.get_secure_cookie("login"))

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
                output_file = open(final_filename, 'wb')
                output_file.write(photos['body'])

                
                    


    def new_post(self):
        """ create the new post in table """
        self.print_file_info()

        self.write("post/new (POST)")
        print("static dir : " + str((dir(self.application))))
        print("static settings : " + str((self.application.settings.keys())))
        print("static handlers : " + str((self.application.handlers)))
        print("static path : " + str((os.path.normpath(self.application.settings["static_path"]))))

        print("stat path handler : " + str(tornado.web.StaticFileHandler._stat))
        title = self.get_argument('post_title', '')
        text = self.get_argument('post_text', '')
        tags = self.get_argument("post_tags", None)
        is_event = self.get_argument("post_is_event", False)
        event = self.get_argument("post_event", None)
        self.write("title: " + title)
        p = Post()
        # p.title = title
        # p.text = text
        # if tags:
        #     p.tags = tags
        # if is_event:
        #     p.event_text = event
        # if photo:
        #     p.photo = final_filename

    def on_finish(self):
        """
            Called after the end of a request.
        """
        pass


