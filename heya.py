# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, abort, redirect, Response, url_for
from netease import netease_cloud_music
import os.path
import sys
import json
import urllib
import requests
from urllib import quote
import subprocess

reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)


def url(file_name=''):
    return 'https://raw.githubusercontent.com/' + quote(str(username).lower()) + '/HeyaData/master/' + quote(
        str(file_name))


curr_path = os.path.dirname(os.path.abspath(__file__))
username = str(os.popen('git config --global --get user.name').read()).replace('\n', '')
curr_commit = str(os.popen('git rev-parse HEAD').read()).replace('\n', '')


@app.route('/pull')
def pull():
    os.system('git pull >.pulllog 2>.pulllog')
    result = open('.pulllog').read()

    config = json.loads(requests.get(url('config.json')).content)

    playlist_id = config['playlist']

    playlist_info = netease_cloud_music("playlist", playlist_id, 0)
    songs_info = playlist_info["songs_info"]
    title = playlist_info["playlist"]

    return render_template('viewer.html', filename='Pull结果', url='',
                           content='# Pull 结果\n```bash\n' + result + '\n```\n[返回首页](/)',
                           config=config, quote=quote, str=str,
                           songs_info=songs_info, title=title, v=curr_commit)


@app.route('/')
@app.route('/<path:filename>')
def view(filename=''):
    config = json.loads(requests.get(url('config.json')).content)
    if filename == '':
        filename = config['index']
    if not filename.endswith('.md'):
        filename += '.md'

    playlist_id = config['playlist']

    playlist_info = netease_cloud_music("playlist", playlist_id, 0)
    songs_info = playlist_info["songs_info"]
    title = playlist_info["playlist"]

    return render_template('viewer.html',
                           filename=filename[:-3], url=url(filename), content='', config=config, quote=quote, str=str,
                           songs_info=songs_info, title=title, v=curr_commit)


if __name__ == "__main__":
    app.run(port=4000)
