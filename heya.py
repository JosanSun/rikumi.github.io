# -*- coding: utf-8 -*-
import json
import os.path
import time
import urllib
import urllib.request
from io import StringIO
from urllib.parse import quote

import requests
from PIL import Image, ImageDraw
from flask import Flask, render_template

app = Flask(__name__)


def url(file_name=''):
    return 'https://raw.githubusercontent.com/' + quote(str(username).lower()) + '/HeyaData/master/' + quote(
        str(file_name))


curr_path = os.path.dirname(os.path.abspath(__file__))
username = str(os.popen('git config --global --get user.name').read()).replace('\n', '')
curr_commit = str(os.popen('git rev-parse HEAD').read()).replace('\n', '')


@app.route('/pull')
@app.route('/pull/')
def pull():
    os.system('git pull >.pulllog 2>.pulllog')
    result = open('.pulllog').read()

    config = json.loads(requests.get(url('config.json')).text)

    return render_template('viewer.html', filename='Pull结果', url='',
                           content='# Pull 结果\n```bash\n' + result + '\n```\n[返回首页](/)',
                           config=config, quote=quote, str=str, v=curr_commit)


@app.route('/show')
@app.route('/show/')
@app.route('/show/<path:filename>')
def show(filename=''):
    config = json.loads(requests.get(url('config.json')).text)
    if filename == '':
        filename = config['index']
    if not filename.endswith('.md'):
        filename += '.md'

    return render_template('shower.html',
                           filename=filename[:-3], url=url(filename), content='', config=config, quote=quote, str=str,
                           v=curr_commit)


@app.route('/')
@app.route('/<path:filename>')
def view(filename=''):
    config = json.loads(requests.get(url('config.json')).text)
    if filename == '':
        filename = config['index']
    if not filename.endswith('.md'):
        filename += '.md'

    return render_template('viewer.html',
                           filename=filename[:-3], url=url(filename), content='', config=config, quote=quote, str=str,
                           v=curr_commit)


last_avatar = 0
last_favicon = 0


@app.route('/apple-icon.png')
def apple_icon():
    global last_avatar

    config = json.loads(requests.get(url('config.json')).text)
    pic_url = config['avatar']
    stamp = int(time.time())
    if stamp > last_avatar + 120:
        # print('Generating new apple icon', stamp)
        urllib.request.urlretrieve(pic_url, 'static/.avatar.png')
        ima = Image.open('static/.avatar.png').convert("RGBA")
        size = ima.size
        r2 = 100
        ima = ima.resize((r2, r2), Image.ANTIALIAS)
        circle = Image.new('L', (r2 * 5, r2 * 5), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, r2 * 5 - 1, r2 * 5 - 1), fill=255)
        circle = circle.resize((r2, r2), Image.ANTIALIAS)
        ima.putalpha(circle)
        bg = Image.new('RGBA', (120, 120), 'white')
        r, g, b, a = ima.split()
        bg.paste(ima, (10, 10), mask=a)
        bg.save('static/.apple-icon.png')
        last_avatar = stamp

    return app.send_static_file('.apple-icon.png')


@app.route('/favicon.png')
def favicon():
    global last_favicon

    config = json.loads(requests.get(url('config.json')).text)
    pic_url = config['avatar']
    stamp = int(time.time())
    if stamp > last_favicon + 120:
        # print('Generating new favicon', stamp)
        urllib.request.urlretrieve(pic_url, 'static/.avatar.png')
        ima = Image.open('static/.avatar.png').convert("RGBA")
        size = ima.size
        r2 = 100
        ima = ima.resize((r2, r2), Image.ANTIALIAS)
        circle = Image.new('L', (r2 * 5, r2 * 5), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, r2 * 5 - 1, r2 * 5 - 1), fill=255)
        circle = circle.resize((r2, r2), Image.ANTIALIAS)
        ima.putalpha(circle)
        ima.save('static/.favicon.png')
        last_favicon = stamp

    return app.send_static_file('.favicon.png')
    

if __name__ == "__main__":
    app.run(port=4000, debug=True)
