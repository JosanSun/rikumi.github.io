# -*- coding: utf-8 -*-
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import StaticFileHandler, RequestHandler


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [  # 请注意所有要输入uuid的位置要用([^/]+)而不是(\w+),否则无法识别旧版应用用户
            (r'/', EditorHandler),
            (r'/static', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'static')}),
            (r'/(.+)', EditorHandler)
        ]
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            template_path=os.path.join(os.path.dirname(__file__), 'template'),
            cookie_secret='365B3932BBBA6182B2D899B494468874',
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.filepath = os.path.join(os.path.dirname(__file__), 'files')


class EditorHandler(BaseHandler):
    def get(self, filename='index.md'):
        filename = filename.replace('/../', '/')
        if not filename.endswith('.md'):
            self.redirect(filename + '.md')
        file_content = u'// New file'
        try:
            file_object = open(os.path.join(os.path.dirname(__file__), 'data', filename))
            try:
                file_content = file_object.read()
            finally:
                file_object.close()
        except:
            pass
        self.render('editor.html', filename=filename, content=file_content)

    def post(self, filename='index.md'):
        data = self.get_argument('data')
        filename = filename.replace('/../', '/')
        if not filename.endswith('.md'):
            self.redirect(filename + '.md')
        file_content = u'// New file'
        try:
            file_object = open(os.path.join(os.path.dirname(__file__), 'data', filename), 'w')
            try:
                file_object.write(data)
            finally:
                file_object.close()
        except:
            pass


if __name__ == '__main__':
    Application().listen(4000)
    tornado.ioloop.IOLoop.instance().start()
