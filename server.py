#!/usr/bin/python3
# -*- coding:utf8 -*-


__author__ = 'Vctcn93'
__version__ = 20190317


from flask import Flask, request
import gibbon
import json


app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to gibbon services!'


@app.route('/create_new_getter')
def create_new_getter():
    name = request.args.get('name')
    pm.create_new_getter(name)
    return 'created new getter'


@app.route('/set_getter_params')
def set_getter_params():
    str_params = request.args.get('params')
    params = json.loads(str_params)
    pm.set_getter_params(params)
    return 'params setted'


@app.route('/set_active_getter')
def set_active_getter():
    index = request.args.get('index')
    pm.set_active_getter(index)
    return f'now your active getter is {pm.getter.name}'


@app.route('/show_all_getter')
def show_all_getter():
    msg = '目前已申请过的请求为：'
    for item in pm.__created_getter:
        msg += '\n' + item[0]
    return msg


@app.route('/get_datas')
def get_datas():
    pm.getter.get_datas()
    return 'data getted'


@app.route('/export_datas')
def export():
    path = request.args.get('path')
    pm.export_getter_data(path)
    return 'data exported'


@app.route('/convert_format')
def convert_format():
    path1 = request.args.get('path1')
    path2 = request.args.get('path2')
    function = request.args.get('func')

    pm.convert_format(path1, path2, function)
    return 'format converted'


if __name__ == '__main__':
    pm = gibbon.ProjectManager()
    app.run(port=5555)
