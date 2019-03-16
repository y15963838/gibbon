#!/usr/bin/python3
# -*- coding:utf8 -*-


__author__ = 'Vctcn93'
__version__ = 20190315


import gibbon
import pytest


class TestAmap:
    @pytest.fixture(scope="class")
    def getter(self):
        return gibbon.Amap()

    def test_function1(self, getter):
        path_1 = r'C:\work\defult_unconvert.csv'
        path_2 = r'C:\work\defult_converted.csv'
        getter.get_datas()
        getter.export(path_1)

        gflnglat = gibbon.pdv.strlocationtofloatlocation(
            getter.dataframe['location']
        )
        wflnglat = gibbon.pdv.gcj02towgs84(gflnglat)
        wslnglat = gibbon.pdv.floatlocationtostrlocation(wflnglat)
        getter.dataframe['location'] = wslnglat
        getter.export(path_2)

        path_3 = r'C:\work\setted_unconvert.csv'
        path_4 = r'C:\work\setted_converted.csv'
        getter.set_city('株洲')
        getter.set_keywords('学校')
        getter.get_datas()
        getter.export(path_3)

        gflnglat = gibbon.pdv.strlocationtofloatlocation(
            getter.dataframe['location']
        )
        wflnglat = gibbon.pdv.gcj02towgs84(gflnglat)
        wslnglat = gibbon.pdv.floatlocationtostrlocation(wflnglat)
        getter.dataframe['location'] = wslnglat
        getter.export(path_4)

    def test_function2(self, getter):
        path_5 = r'C:\work\defult_unconvert2.csv'
        path_6 = r'C:\work\defult_converted2.csv'
        getter.reset()
        getter.set_function('1')
        getter.get_datas()
        getter.export(path_5)

        gflnglat = gibbon.pdv.strlocationtofloatlocation(
            getter.dataframe['location']
        )
        wflnglat = gibbon.pdv.gcj02towgs84(gflnglat)
        wslnglat = gibbon.pdv.floatlocationtostrlocation(wflnglat)
        getter.dataframe['location'] = wslnglat
        getter.export(path_6)

        path_7 = r'C:\work\setted_unconvert2.csv'
        path_8 = r'C:\work\setted_converted2.csv'
        location = '113.067325,27.838871'
        wflnglat = gibbon.strlocationtofloatlocation(location)
        gflnglat = gibbon.wgs84togcj02(wflnglat[0], wflnglat[1])
        gslnglat = gibbon.floatlocationtostrlocation(gflnglat)
        getter.set_location(gslnglat)
        getter.set_radius('5000')
        getter.set_keywords('公交站')
        getter.get_datas()
        getter.export(path_7)

        gflnglat = gibbon.pdv.strlocationtofloatlocation(
            getter.dataframe['location']
        )
        wflnglat = gibbon.pdv.gcj02towgs84(gflnglat)
        wslnglat = gibbon.pdv.floatlocationtostrlocation(wflnglat)
        getter.dataframe['location'] = wslnglat
        getter.export(path_8)
