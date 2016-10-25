# -*- coding: utf-8 -*-
import os.path
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import uuid
import re
import threading
from threading import Timer
from tornado.web import StaticFileHandler, RequestHandler

reload(sys)
sys.setdefaultencoding('utf8')

lock = threading.Lock()
conflict_head = re.compile(r'<<<<<<< HEAD')
conflict_split = re.compile(r'=======')
conflict_tail = re.compile(r'>>>>>>> [0-9a-f]{8}')
blacklines = re.compile(r'\n+$')

branches = set()
timers = dict()
timeout = 600


def data_path(file_name=''):
    if file_name == '':
        return os.path.join(os.path.dirname(__file__), 'data')
    return os.path.join(os.path.dirname(__file__), 'data', file_name)


def command(string):
    if os.path.isfile(data_path()):
        os.system('cd ' + os.path.dirname(__file__) + ' && rm -f data')
    if not os.path.exists(data_path()):
        os.system('cd ' + os.path.dirname(__file__))
        os.system('mkdir data')
    os.system('cd ' + os.path.join(os.path.dirname(__file__), 'data') + ' && ' + string)


def read_file(filename, default=''):
    file_content = default
    try:
        file_object = open(data_path(filename))
        try:
            file_content = file_object.read()
        finally:
            file_object.close()
    except:
        pass
    return file_content


def write_file(filename, data):
    try:
        file_object = open(data_path(filename), 'w')
        try:
            file_object.write(data)
        finally:
            file_object.close()
    except:
        pass


def schedule_delete_branch(branch):
    if branch in timers:
        timers[branch].cancel()

    def timer_func():
        branches.remove(branch)
        command('git branch -d ' + branch)

    timer = Timer(timeout, timer_func)


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


class EditorHandler(BaseHandler):
    def get(self, filename=''):
        filename = filename.replace('/../', '/')
        if filename == '':
            self.redirect('index.md')
            return
        if not filename.endswith('.md'):
            self.redirect(filename + '.md')
            return
        file_content = read_file(filename, default=u'// 这是一个新文件，你可以在此随意发挥。')

        branch = str(uuid.uuid4())[:8]

        command('git branch ' + branch)
        branches.add(branch)

        self.render('editor.html', filename=filename, content=file_content, branch=branch)
        schedule_delete_branch(branch)

    def post(self, filename='index.md'):
        # 不允许异步访问, 防止写入到错误的分支
        with lock:
            if self.get_argument('data', default=None) is not None:
                data = self.get_argument('data').decode('utf8')
                branch = self.get_argument('branch')
                filename = filename.replace('/../', '/')
                if not filename.endswith('.md'):
                    self.write(u'// 文件名不合法，保存失败。\n' + data)
                    return

                if branch not in branches:
                    self.write(u'// 会话已超时，保存失败。请备份内容并刷新页面后再试。\n' + data)
                    return

                # 切换到该用户所在分支
                command('git checkout ' + branch)

                # 执行更改
                write_file(filename, data)

                # 提交并推送, 此时可能会出现冲突
                command('git add * && git commit -m "Saved by remote user"')
                command('git checkout master && git merge ' + branch + ' -m "Auto-merged"')

                self.auto_fix_conflict(filename)
                command('git checkout ' + branch + ' && git merge master -m "Auto-backmerged" && git checkout master')
                schedule_delete_branch(branch)

            self.write(read_file(filename))

    def auto_fix_conflict(self, filename):
        file_content = read_file(filename)
        file_content = blacklines.sub('', file_content)
        if file_content.find("<<<<<<< HEAD") >= 0:
            file_content = conflict_head.sub(u'//! 此处发生编辑冲突。其他人编辑的版本：', file_content)
            file_content = conflict_split.sub(u'//! 你的版本：', file_content)
            file_content = conflict_tail.sub(u'//! 请及时解决本冲突并删除这段注释。', file_content)
            file_content = u'// 文件已被其他人编辑，请解决文件中的冲突并保存。\n' + file_content
            write_file(filename, file_content)
            command('git add * && git commit -m "Fixed conflict"')


if __name__ == '__main__':
    if not os.path.exists(data_path('.git')):
        print 'First time to run. Initializing...'
        command('git config user.email "nobody@example.com"')
        command('git config user.name "nobody"')
        command('git init && git checkout -b master && touch index.md && git add * && git commit -m "Original data"')
        print 'Initialization complete. Have fun!'
    Application().listen(4000)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except:
        for branch in branches:
            command('git branch -d ' + branch)
