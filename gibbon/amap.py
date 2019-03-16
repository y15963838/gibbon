#!/usr/bin/python3
# -*- coding:utf8 -*-


__author__ = 'Vctcn93'
__version__ = 20190315


"""
╔═════════════════════════════════════╗
║ 提供查询通过高德开发者平台拿取 API 的方法 ║
╚═════════════════════════════════════╝
AUTHUR：VCTCN93   VERSION：1.00BATA
══════════════════════════════════════════════════════════════════════════════════

该模块分两种请求方法，所有输入均为字符：
    ║ 
    ╠═ 以 城市 和 查询关键字 为基础，在城市范围内搜索符合条件的 POI。
    ║  其功能代码为 '1'
    ║ 
    ╚═ 以项 目中心点、搜索半径、查询关键字 为基础，拿取项目中心点周边的 POI。
       其功能代码为 '2'
       在输入字符格式的项目坐标时，切忌','，附近有空格，否则高德将无法识别此坐标
       
"""


import urllib.request
import pandas as pd
import json
import re


class Amap:
    """
    一个包含了拿取高德 POI 的方法
    """
    # 定义一些不许用户修改的参数
    __user_key: str = 'fa1eac0178bc74acca33d7e874470704'  # 高德开发者密钥
    __citylimit: str = 'false'  # 是否仅返回城市 API
    __children: str = '0'  # 子层级数
    __offset: str = '20'  # 每页 POI 个数
    __page: str = '1'  # 当前页面数
    __building: str = ''  # 建筑物的 POI 编号，传入建筑物POI编号之后，则只在该建筑物之内进行搜索
    __floor: str = ''  # 搜索楼层
    __extensions: str = 'base'  # 返回结果控制，all 为返回地址信息、附近POI、道路以及道路交叉口信息
    __sig: str = ''  # 电子签名
    __output: str = 'JSON'  # 拿取格式
    __callback: str = ''  # 用户定义的函数名称，此参数只在output=JSON时有效
    __sortrule = 'distance'  # 排序规则
    __types: str = ''  # 搜索类别

    def __init__(
            self,
            keywords: str = '地铁站',
            city: str = '广州',
            location: str = '113.32613620923807,23.13869440310364',
            radius: str = '3000',
            function: str = '0',
            # TODO: project_name: str = 'Defult Name'
    ):
        """
        设置一次查询项
        :param keywords: 查询关键字，多个关键字用“|”分割
        :param city: 查询城市
        :param location: wgs84 下中心点坐标，经度和纬度用","分割，切忌坐标间有空格
                        经度在前，纬度在后，经纬度小数点后不得超过6位。
        :param radius: 查询半径，单位为米
        :param function: 功能代码，0 为查询城市尺度 POI，1 为查询周边尺度 POI
        """
        self.keywords: str = keywords
        self.city: str = city
        self.location: str = location
        self.radius: str = radius
        self.function: str = function
        self.__count: int = None
        self.dataframe: pd.DataFrame = None
        # TODO: self.name = project_name

    def set_keywords(self, keyword: str) -> None:
        """
        设置查询关键字
        :param keyword: 查询关键字
        :return: None
        """
        self.keywords = keyword

    def set_city(self, city: str) -> None:
        """
        设置查询城市
        :param city: 查询城市
        :return: None
        """
        self.city = city

    def set_location(self, location: str) -> None:
        """
        设置查询中心经纬坐标（gcj02）
        :param location: 查询中心经纬坐标（gcj02）
        :return: None
        """
        self.location = location

    def set_radius(self, radius: str) -> None:
        """
        设置查询半径
        :param radius: 查询半径，米为单位
        :return: None
        """
        self.radius = radius

    def set_function(self, function_number: str) -> None:
        """
        设置查询功能代码
        :param function_number: 设置查询功能代码, '0' 为查询城市级别； '1' 为查询项目周边
        :return: None
        """
        self.function = function_number

    def reset(self) -> None:
        """
        将所有值更改为默认
        :return: None
        """
        self.keywords: str = '地铁站'
        self.city: str = '广州'
        self.location: str = '113.32613620923807,23.13869440310364'
        self.radius: str = '3000'
        self.function: str = '0'
        self.__count: int = None
        self.dataframe: pd.DataFrame = None

    def __set_count_and_dataframe(self):
        """
        设置改次爬取的 POI 数量与需要的 DataFrame
        :return: None
        """
        response = urllib.request.urlopen(self.__work_url)
        dict_ = json.loads(response.read(), encoding='utf_8_sig')

        self.__count = int(dict_['count'])

        if len(dict_['pois']) == 0:
            raise Warning('该坐标周边没有目标点，请检查输入坐标点，请输入其它坐标再次尝试')

        columns = list(dict_['pois'][0].keys())
        dataframe = pd.DataFrame(columns=columns)

        self.dataframe = dataframe

    @property
    def city_url(self) -> str:
        """
        生成一个用于爬取城市尺度的高德 url
        :return: url
        """
        url = 'https://restapi.amap.com/v3/place/text?' \
              + 'key=' + str(urllib.request.quote(self.__user_key)) \
              + '&keywords=' + str(urllib.request.quote(self.keywords)) \
              + '&types=' + str(urllib.request.quote(self.__types)) \
              + '&city=' + str(urllib.request.quote(self.city)) \
              + '&citylimit=' + str(urllib.request.quote(self.__citylimit)) \
              + '&children=' + str(urllib.request.quote(self.__children)) \
              + '&offset=' + str(urllib.request.quote(self.__offset)) \
              + '&page=' + str(urllib.request.quote(self.__page)) \
              + '&building=' + str(urllib.request.quote(self.__building)) \
              + '&floor=' + str(urllib.request.quote(self.__floor)) \
              + '&extensions=' + str(urllib.request.quote(self.__extensions)) \
              + '&sig=' + str(urllib.request.quote(self.__sig)) \
              + '&output=' + str(urllib.request.quote(self.__output)) \
              + '&callback=' + str(urllib.request.quote(self.__callback))
        return url

    @property
    def around_url(self) -> str:
        """
        生成一个用于项目周边的高德 url
        :return: url
        """
        url = 'https://restapi.amap.com/v3/place/around?' \
              + 'key=' + str(urllib.request.quote(self.__user_key)) \
              + '&location=' + str(urllib.request.quote(self.location)) \
              + '&keywords=' + str(urllib.request.quote(self.keywords)) \
              + '&types=' + str(urllib.request.quote(self.__types)) \
              + '&city=' + str(urllib.request.quote(self.city)) \
              + '&radius=' + str(urllib.request.quote(self.radius)) \
              + '&sortrule=' + str(urllib.request.quote(self.__sortrule)) \
              + '&offset=' + str(urllib.request.quote(self.__offset)) \
              + '&page=' + str(urllib.request.quote(self.__page)) \
              + '&extensions=' + str(urllib.request.quote(self.__extensions)) \
              + '&sig=' + str(urllib.request.quote(self.__sig)) \
              + '&output=' + str(urllib.request.quote(self.__output)) \
              + '&callback=' + str(urllib.request.quote(self.__callback))
        return url

    @property
    def __work_url(self):
        return self.city_url if self.function == '0' else self.around_url

    def get_datas(self):
        """
        向数据库里添加爬得的高德 POI 点
        :return: None
        """
        self.__set_count_and_dataframe()

        rounds = int(self.__count / 20) + 1

        for i in range(1, rounds + 1):
            each_url = re.sub(r'page=\d*', f'page={i}', self.__work_url)
            response = urllib.request.urlopen(each_url)
            dict_ = json.loads(response.read(), encoding='utf_8_sig')
            pois = dict_['pois']
            dataframe = pd.DataFrame(pois)
            self.dataframe = self.dataframe.append(dataframe, sort=True)

        self.dataframe.reset_index(drop=True, inplace=True)

    def export(self, path: str) -> None:
        """
        将爬得的数据以 CSV 格式导出到路径
        :param path: 需要导出到的路径
        :return: None
        """
        self.dataframe.to_csv(path, encoding='utf_8_sig')

    @classmethod
    def get_config(cls) -> dict:
        """
        以字典的形式返回当前 Amap 的配置
        :return: dict
        """
        return {
            'user_key': cls.__user_key,  # 高德开发者密钥
            'citylimit': cls.__citylimit,  # 是否仅返回城市 API
            'children': cls.__children,  # 子层级数
            'offset': cls.__offset,  # 每页 POI 个数
            'page': cls.__page,  # 当前页面数
            'building': cls.__building,  # 建筑物的 POI 编号，传入建筑物POI编号之后，则只在该建筑物之内进行搜索
            'floor': cls.__floor,  # 搜索楼层
            'extensions': cls.__extensions,  # 返回结果控制，all 为返回地址信息、附近POI、道路以及道路交叉口信息
            'sig': cls.__sig,  # 电子签名
            'output': cls.__output,  # 拿取格式
            'callback': cls.__callback,  # 用户定义的函数名称，此参数只在output=JSON时有效
            'sortrule': cls.__sortrule,  # 排序规则
            'types': cls.__types  # 搜索类别
        }

    @classmethod
    def export_config(cls, path) -> None:
        """
        导出当前的 Amap 配置为 JSON 文件
        :param path: 导出路径
        :return: None
        """
        config = str(cls.get_config())
        with open(path, 'w', encoding='utf-8') as obj:
            obj.write(config)

    @classmethod
    def set_config(cls, path):
        """
        通过 JSON 配置文件更改 Amap 配置
        :return: None
        """
        with open(path, 'r', encoding='utf-8') as obj:
            file = eval(obj.read())

        for key, value in file.items():
            if key == 'user_key':
                cls.__user_key = value
            if key == 'citylimit':
                cls.__citylimit = value
            if key == 'children':
                cls.__children = value
            if key == 'offset':
                cls.__offset = value
            if key == 'page':
                cls.__page = value
            if key == 'building':
                cls.__building = value
            if key == 'floor':
                cls.__floor = value
            if key == 'extensions':
                cls.__extensions = value
            if key == 'sig':
                cls.__sig = value
            if key == 'output':
                cls.__output = value
            if key == 'callback':
                cls.__callback = value
            if key == 'sortrule':
                cls.__sortrule = value
            if key == 'types':
                cls.__types = value
