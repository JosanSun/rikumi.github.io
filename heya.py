# -*- coding: utf-8 -*-
import os.path
import sys
import json
import urllib
from urllib import quote
import subprocess
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.gen import Task
from tornado.web import StaticFileHandler, RequestHandler
from tornado.httpclient import HTTPRequest, HTTPClient

reload(sys)
sys.setdefaultencoding('utf8')


def url(file_name=''):
    return 'https://raw.githubusercontent.com/' + quote(str(username)) + '/HeyaData/master/' + quote(str(file_name))


def get(file, default_file='', default_content=''):
    try:
        client = HTTPClient()
        request = HTTPRequest(url(file), method='GET', request_timeout=10)
        response = client.fetch(request)
        return response.body
    except:
        if default_file == '':
            return default_content
        else:
            try:
                client = HTTPClient()
                request = HTTPRequest(url(default_file), method='GET', request_timeout=10)
                response = client.fetch(request)
                return response.body
            except:
                return default_content


curr_path = os.path.dirname(os.path.abspath(__file__))
username = str(os.popen('git config --global --get user.name').read()).replace('\n', '')


class Config:
    def __init__(self, json_data):
        self.json_data = json.loads(json_data)

    def __getattr__(self, item):
        try:
            return self.json_data[item]
        except KeyError:
            return ''


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass


class GitPullHandler(BaseHandler):
    def get(self):
        result = subprocess.Popen('git pull'.split(), stdout=subprocess.PIPE).communicate()[0]
        config = Config(get('config.json', default_content='{}'))
        self.render('viewer.html',
                    filename='Pull结果',
                    content='# Pull 结果\n```\n' + result + '\n```\n[返回首页](/)',
                    config=config,
                    quote=quote)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/pull', GitPullHandler),
            (r'/static', StaticFileHandler, {'path': os.path.join(curr_path, 'static')}),
            (r'/(.*)', ViewerHandler),
        ]
        settings = dict(
            debug=True,
            static_path=os.path.join(curr_path, 'static'),
            template_path=os.path.join(curr_path, 'template'),
            cookie_secret='365B3932BBBA6182B2D899B494468874',
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class ViewerHandler(BaseHandler):
    def get(self, filename=''):
        config = Config(get('config.json', default_content='{}'))
        if filename == '':
            filename = config.index
        if not filename.endswith('.md'):
            filename += '.md'
        file_content = get(filename, default_file='404.md')

        self.render('viewer.html', filename=filename[:-3], content=file_content, config=config, quote=quote)


if __name__ == '__main__':
    Application().listen(4000)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except:
        pass
