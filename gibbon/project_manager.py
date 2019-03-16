#!/usr/bin/python3
# -*- coding:utf8 -*-


__author__ = 'Vctcn93'
__version__ = 20190315


from gibbon import Amap
import time


class ProjectManager:
    __created_instance = None  # 已创建的实例
    __created_project = list()  # 已创建的请求

    def __new__(cls, *args, **kwargs):
        """
        使用单例模式，确保全局有且仅有一个 Amap 实例被创建
        :param args: 传参
        :param kwargs: 传参
        :return: Amap instance
        """
        if cls.__created_instance is None:
            instance = super().__new__(cls)
            cls.__created_instance = instance
        return cls.__created_instance

    def create_project(self, name: str = 'Defult Name'):
        key = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\t' + name
        getter = Amap()
        self.__created_project.append([key, getter])
        return getter

    def show_all_project(self) -> None:
        """
        显示目前已经申请过的所有请求
        :return: None
        """
        msg = '目前已申请过的请求为：\n'

        for item in self.__created_project:
            msg += item[0] + '\n'

        print(msg)

    def get_project(self, index):
        return self.__created_project[index][1]

    def remove_project(self, key):
        del self.__created_project[key]
