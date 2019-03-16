#!/usr/bin/python3
# -*- coding:utf8 -*-


__author__ = 'Vctcn93'
__version__ = 20190315


"""
MODULE：CONVERTOR_PANDAS_VERSION
╔════════════════════════════════╗
║ 直接运算 series，来转换坐标系与格式 ║
╚════════════════════════════════╝
AUTHUR：VCTCN93   VERSION：1.00BATA
══════════════════════════════════════════════════════════════════════════════════

╔═ 地心坐标 (WGS84)
║    国际标准，从 GPS 设备中取出的数据的坐标系
║    国际地图提供商使用的坐标系
║
╠═ 火星坐标 (GCJ-02)也叫国测局坐标系
║    中国标准，从国行移动设备中定位获取的坐标数据使用这个坐标系
║    国家规定： 国内出版的各种地图系统（包括电子形式），必须至少采用GCJ-02对地理位置进行首次加密
║
╠═ 百度坐标 (BD-09)
║    百度标准，GCJ-02 的二次加密
║    百度 SDK，百度地图，Geocoding 使用
║ 
╚═ 墨卡托平面坐标（Mercator）
     将某个坐标系的经纬度，以某一点为中心，转换成二维平面的坐标

"""

# TODO: 求证使用 apply 与直接使用 series 运算的速度差异


import gibbon
import pandas as pd


def wgs84togcj02(lnglat: pd.Series) -> pd.Series:
    return lnglat.apply(lambda x: gibbon.wgs84togcj02(x[0], x[1]))


def wgs84tobd09(lnglat: pd.Series) -> pd.Series:
    return lnglat.apply(lambda x: gibbon.wgs84tobd09(x[0], x[1]))


def gcj02towgs84(lnglat: pd.Series) -> pd.Series:
    return lnglat.apply(lambda x: gibbon.gcj02towgs84(x[0], x[1]))


def gcj02tobd09(lnglat: pd.Series) -> pd.Series:
    return lnglat.apply(lambda x: gibbon.gcj02tobd09(x[0], x[1]))


def bd09towgs84(lnglat: pd.Series) -> pd.Series:
    return lnglat.apply(lambda x: gibbon.bd09towgs84(x[0], x[1]))


def bd09togcj02(lnglat: pd.Series) -> pd.Series:
    return lnglat.apply(lambda x: gibbon.bd09togcj02(x[0], x[1]))


def lnglattomercator(
        lnglat: pd.Series,
        reference_position: list = (0, 0),
        convert_rate: list = (1, 1)
) -> pd.Series:
    return lnglat.apply(lambda x: gibbon.lnglattomercator(
        x[0],
        x[1],
        reference_position,
        convert_rate
    )
                        )


def strlocationtofloatlocation(lnglat: pd.Series) -> pd.Series:
    return lnglat.apply(gibbon.strlocationtofloatlocation)


def floatlocationtostrlocation(lnglat: pd.Series) -> pd.Series:
    return lnglat.apply(gibbon.floatlocationtostrlocation)

