# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, abort, redirect, Response, url_for
import os.path
import json
import urllib
import requests
from urllib.parse import quote
import subprocess

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


if __name__ == "__main__":
    app.run(port=4000, debug=True)
