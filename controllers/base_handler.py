import tornado.web
from tornado.log import app_log
import tornado.escape
import pprint

import os
import json
import re
from tinydb import TinyDB, where


reg_b = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows ce|xda|xiino", re.I|re.M)
reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)

class BaseHandler(tornado.web.RequestHandler):

    #
    # Base Handler for the Controllers 
    #

    def initialize(self):
        self.default_methods = {}
        self.default_methods = {}

    def get_current_user(self):
        login = self.get_secure_cookie("login")
        return str(login.decode("utf-8"))

    def write_debug_info(self):
        """
            Called at the beginning of a request before get/post/etc.
        """
        #path = self.request.uri.split('?')[0]
        #method = path.split('/')[-1]
        
        self.write("Handler: " + str(self.__class__.__name__)+"<br>")
        self.write("<hr>")
        self.write(str(dir(self.request)))
        self.write("<br><hr>")
        self.write("query_arguments:" + str(self.request.query_arguments))
        self.write("<br>")
        self.write("uri:" + self.uri)
        self.write("<br>")
        self.write("path:" + self.path)
        self.write("<br>")
        self.write("method to call: " + self.request.method.lower() + "_" + self.method)
        self.write("<hr>")
        self.write("request method: " + self.request.method)
        self.write("<hr>")
        self.write("request headers: " + str(self.request.headers))
        self.write("<hr>")
        self.flush()

    def is_mobile_request(self, user_agent):
        self.request.mobile = False
        b = reg_b.search(user_agent)
        v = reg_v.search(user_agent[0:4])
        if b or v:
            #return HttpResponseRedirect("http://detectmobilebrowser.com/mobile")
            self.request.mobile = True
            return True
        else:
            return False

    def prepare_routes_classic(self):
        #
        # get controller, method and parameter 
        # for now : /controller/method/parameter1/parm2.../paramN
        #  calls (controller.method(parameters=[param1, param2, ..., paramN])
        #
        print("reverse_url= " + str(self.application.reverse_url))
        self.uri = self.request.uri
        self.path = self.request.uri.split('?')[0]

        if self.path.count("/") > 2:
            self.controller = self.path.split("/")[-3]
            self.method = self.path.split('/')[-2]        
            self.parameter = self.path.split("/")[-1]
        else:
            self.controller = self.path.split("/")[-2]
            self.method = self.path.split('/')[-1]        
       
        return

    def prepare_routes_resty(self):
        self.uri = self.request.uri
        self.path = self.request.uri.split('?')[0]

        paramlist =[]
        controller = ""
        method = ""
        url = self.path
        print(url)
        controller = url.split("/")[1]
        if url.count("/") > 1:
            method = url.split("/")[2]
        if url.count("/") > 2:
            for elem in range(3, url.count("/")+1):
                paramlist.append(url.split("/")[elem])


        print("controller: " + controller)
        print("method: " + method)
        print("params: " + str(paramlist))
        print()
        self.controller = controller
        self.method = method
        self.param_list = paramlist
        return

    def prepare(self):
        """
            Called at the beginning of a request before get/post/etc.
        """
        #self.prepare_routes_classic()
        self.prepare_routes_resty()
        self.default_methods = {}
        #
        # You can use the before_handler in a local controller to
        # process your own prepare stuff.
        # a common use case is to call: self.print_debug_info().
        # which then applies only to this specific handler.
        # 
        before_handler = getattr(self, "before_handler", None)
        print("calling before_handler for " +  str(self.__class__))
        if callable(before_handler):
            before_handler()
        
    def post(self, *args, **kwargs):
        return self.dispatch(self.path, self.method, *args, **kwargs)
    
    def get(self, *args, **kwargs):
        return self.dispatch(self.path, self.method, *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.dispatch(self.path, self.method, *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.dispatch(self.path, self.method, *args, **kwargs)

    def exec_action(self, action, *args, **kwargs):
        if callable(action):
            print("exec_action: *args: " + str(*args))
            print("exec_action: *kwargs: " + str(*kwargs))
            return action(*args, **kwargs)
        else:
            raise tornado.web.HTTPError(404)
    

    def dispatch(self, path, method, *args, **kwargs):
        print("request: " + str(self.request))
        print("dispatch: http request method: " + self.request.method.lower())
        print("dispatch: uri: " +  self.uri)
        #print("dispatch: request dir: " +  str(dir(self.request)))
        print("dispatch: method: " +  self.method)
        print("dispatch: looking for action: " +  method + "_" + self.request.method.lower())
        if "User-Agent" in self.request.headers:
            is_mobile_request = self.is_mobile_request(self.request.headers["User-Agent"])
        else:
            is_mobile_request = False
            print("No User-Agent header given")
        print("dispath is mobile access: " + str(is_mobile_request))
        
        # action name is method + HTTP request method
        action_name = method + "_" + self.request.method.lower()
    
        if is_mobile_request:
            # check if the handler offers a _special_ mobile method to process the request
            print("trying to find the mobile action: " +str(action_name + "_mobile"))
            if hasattr(self, action_name + "_mobile"):
                # go for the mobile method
                action = getattr(self, action_name + "_mobile", None)
                print("dispatch: action is: " + str(action_name + "_mobile"))
                return self.exec_action(action)(*args, **kwargs)
        
        if hasattr(self, action_name ):
            # go for the standard method
            action = getattr(self, action_name, None)
            print("dispatch: action is: " + str(action_name))
            return self.exec_action(action)
        elif self.request.method.lower() in self.default_methods:
            # check if there is a default action for this http request type and call that
            # this gives: get_login() if self.default_methods["get"] = "login"
            action = getattr(self, self.default_methods[self.request.method.lower()] + "_" + self.request.method.lower())
            return action()
        else:
            # error, controller doesnt offer such a reuest method.
            raise tornado.web.HTTPError(404)
    

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('errors/404.tmpl',page=self.path)
        else:
            self.render('errors/unknown.tmpl',page=self.path)

