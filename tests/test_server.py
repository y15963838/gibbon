#!/usr/bin/python3
# -*- coding:utf8 -*-


__author__ = 'Vctcn93'
__version__ = 20190317


import urllib.request
import pytest
import json


class TsetFunction1:
    @pytest.fixture(scope="class")
    def link(self):
        return "localhost:5555/"

    def test_create_new_getter(self, link):
        cmd = 'create_new_getter?'
        param = "name=成都地铁站查询"
        url = link + cmd + param
        url = url.replace('"', "'")
        response = urllib.request.urlopen(url)
        claim = json.loads(response.read())
        assert claim == 'created new getter'

    def test_set_getter_params(self, link):
        cmd = 'set_getter_params?'
        param = "{'city':'成都','keywords':'地铁站'}"
        url = link + cmd + param
        url = url.replace('"', "'")
        response = urllib.request.urlopen(url)
        claim = json.loads(response.read())
        assert claim == 'params setted'

    def test_get_datas(self, link):
        cmd = 'get_datas?'
        url = link + cmd
        url = url.replace('"', "'")
        response = urllib.request.urlopen(url)
        claim = json.loads(response.read())
        assert claim == 'data getted'

    def test_export(self, link):
        cmd = 'export_datas?'
        param = 'path=ChengduMetro.csv'
        url = link + cmd + param
        url = url.replace('"', "'")
        response = urllib.request.urlopen(url)
        claim = json.loads(response.read())
        assert claim == 'data exported'

    def test_convert_format(self, link):
        cmd = 'convert_format?'
        param = 'path1=ChenduMetro.csv&path2=Chengdumetro.geojson&func=csvtogeojson'
        url = link + cmd + param
        url = url.replace('"', "'")
        response = urllib.request.urlopen(url)
        claim = json.loads(response.read())
        assert claim == 'format converted'


class TsetFunction2:
    @pytest.fixture(scope="class")
    def link(self):
        return 'localhost:5555/'

    def test_create_new_getter(self, link):
        cmd = 'create_new_getter?'
        param = "name=经纬坐标医院查询"
        url = link + cmd + param
        url = url.replace('"', "'")
        response = urllib.request.urlopen(url)
        claim = json.loads(response.read())
        assert claim == 'created new getter'

    def test_set_getter_params(self, link):
        cmd = 'set_getter_params?'
        param = "{'location':'113.00036,28.19782','keywords':'医院','radius'='5000','function'='1'}"
        url = link + cmd + param
        url = url.replace('"', "'")
        response = urllib.request.urlopen(url)
        claim = json.loads(response.read())
        assert claim == 'params setted'

    def test_get_datas(self, link):
        cmd = 'get_datas?'
        url = link + cmd
        url = url.replace('"', "'")
        response = urllib.request.urlopen(url)
        claim = json.loads(response.read())
        assert claim == 'data getted'

    def test_export(self, link):
        cmd = 'export_datas?'
        param = 'path=ChangShaYiYuan.csv'
        url = link + cmd + param
        url = url.replace('"', "'")
        response = urllib.request.urlopen(url)
        claim = json.loads(response.read())
        assert claim == 'data exported'

    def test_convert_format(self, link):
        cmd = 'convert_format?'
        param = 'path1=ChangShaYiYuan.csv&path2=ChangShaYiYuan.geojson&func=csvtogeojson'
        url = link + cmd + param
        url = url.replace('"', "'")
        response = urllib.request.urlopen(url)
        claim = json.loads(response.read())
        assert claim == 'format converted'


class TestOther:
    @pytest.fixture(scope="class")
    def link(self):
        return 'localhost:5555/'

    def test_getter_exchange(self, link):
        cmd = 'set_active_getter?'
        param = '0'
        url = link + cmd + param
        url = url.replace('"', "'")
        response = urllib.request.urlopen(url)
        claim = json.loads(response.read())
        assert claim == 'now your active getter is 成都地铁站查询'
