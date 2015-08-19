#
# One Tornado UIModule to render them all ;)
#
import tornado.web

class RenderPatialModule(tornado.web.UIModule):
	def render(self, partial=None):
		return "<h1>Hello, world!</h1><p>" + str(partial) + "</p>"