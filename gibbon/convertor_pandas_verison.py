#!/usr/bin/python3
# -*- coding:utf8 -*-


__author__ = 'Vctcn93'
__version__ = 20190315


"""
MODULE：CONVERTOR_PANDAS_VERSION
╔═══════════════════════════════════════════════╗
║ 使用 numpy 与 pandas 的向量运算，来转换坐标系与格式 ║
╚═══════════════════════════════════════════════╝
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

══════════════════════════════════════════════════════════════════════════════════

╔═ 支持GIS中各种常用格式的互相转换：
║    JSON
║    GeoJSON
║    CSV
║
╠═ 本库基准坐标：
║    WGS-84，代号 EPSG:4326
║
╚═ 标准的GeoJson文件格式如下：
    {
        "type": "FeatureCollection",
        "name": 文件名,
        "crs": { 
            "type": "name", 
            "properties": { 
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            } 
        },
        "features": [
            {
                "type":"Feature",
                "properties":{},
                "geometry":{
                    "type":"Point"(或者"LineString", "Polygon"),
                    "coordinates":[]
                }
            }
        ]
    }

"""


import gibbon.constance as constance
import pandas as pd
import numpy as np
import json


def _transform_lng(lng, lat) -> pd.Series:
    """
    经度常数转换
    :param lng: pd.Series 经度序列
    :param lat: pd.Series 纬度序列
    :return: pd.Series
    """
    ret = 300 + lng + 2 * lat + .1 * lng * lng + .1 * lng * lat + .1 * np.sqrt(np.abs(lng))

    ret += (20 * np.sin(6 * lng * constance.PI) + 20 *
            np.sin(2.0 * lng * constance.PI)) * 2 / 3

    ret += (20 * np.sin(lng * constance.PI) + 40 *
            np.sin(lng / 3 * constance.PI)) * 2 / 3

    ret += (150 * np.sin(lng / 12 * constance.PI) + 300 *
            np.sin(lng / 30.0 * constance.PI)) * 2 / 3

    return ret


def _transform_lat(lng, lat) -> pd.Series:
    """
    纬度常数转换
    :param lng: pd.Series 经度序列
    :param lat: pd.Series 纬度序列
    :return: pd.Series
    """
    ret = -100 + 2 * lng + 3 * lat + .2 * lat * lat + .1 * lng * lat + .2 * np.sqrt(np.abs(lng))

    ret += (20 * np.sin(6 * lng * constance.PI) + 20 *
            np.sin(2.0 * lng * constance.PI)) * 2.0 / 3.0

    ret += (20.0 * np.sin(lat * constance.PI) + 40.0 *
            np.sin(lat / 3.0 * constance.PI)) * 2.0 / 3.0

    ret += (160.0 * np.sin(lat / 12.0 * constance.PI) + 320 *
            np.sin(lat * constance.PI / 30.0)) * 2.0 / 3.0

    return ret


def _is_out_of_china(lng, lat) -> bool:
    """
    判断是否在国内，不在国内返回True，在国内返回False
    :param lng: pd.Series 经度序列
    :param lat: pd.Series 纬度序列
    :return: bool
    """
    if True in lng < 72.004 \
            or True in lng > 137.8347 \
            or True in lat < .9293 \
            or True in lat > 55.8271:
        return True
    return False


def wgs84togcj02(lng, lat) -> list:
    """
    将wgs84坐标系转为火星坐标
    :param lng: pd.Series 经度序列
    :param lat: pd.Series 纬度序列
    :return: list[float] 经纬度序列数组
    """
    if _is_out_of_china(lng, lat):  # 如果不在国内
        return [lng, lat]  # 不做转换

    dlng = _transform_lng(lng - 105, lat - 35)
    dlat = _transform_lat(lng - 105, lat - 35)

    radlat = lat / 180 * constance.PI
    magic = np.sin(radlat)
    magic = 1 - constance.EE * magic * magic
    sqrtmagic = np.sqrt(magic)

    dlat = np.multiply(dlat, 180) / ((constance.A * (1 - constance.EE)) / (magic * sqrtmagic) * constance.PI)
    dlng = np.multiply(dlng, 180) / (constance.A / sqrtmagic * np.cos(radlat) * constance.PI)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def wgs84tobd09(lng, lat) -> list:
    """
    将wgs84坐标系转为百度坐标
    :param lng: pd.Series 经度序列
    :param lat: pd.Series 纬度序列
    :return: list[float] 经纬度序列数组
    """
    if _is_out_of_china(lng, lat):
        return [lng, lat]
    gcjlng, gcjlat = wgs84togcj02(lng, lat)
    bdlng, bdlat = gcj02tobd09(gcjlng, gcjlat)
    return [bdlng, bdlat]


def gcj02towgs84(lng, lat) -> list:
    """
    将火星坐标系转为wgs84坐标
    :param lng: pd.Series 经度序列
    :param lat: pd.Series 纬度序列
    :return: list[pd.Series] 经纬度序列数组
    """
    if _is_out_of_china(lng, lat):
        return [lng, lat]

    dlat = _transform_lat(lng - 105, lat - 35)
    dlng = _transform_lng(lng - 105, lat - 35)

    radlat = lat / 180 * constance.PI
    magic = np.sin(radlat)
    magic = 1 - constance.EE * magic * magic
    sqrtmagic = np.sqrt(magic)

    dlat = np.multiply(dlat, 180) / ((constance.A * (1 - constance.EE)) / (magic * sqrtmagic) * constance.PI)
    dlng = np.multiply(dlng, 180) / (constance.A / sqrtmagic * np.cos(radlat) * constance.PI)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def gcj02tobd09(lng, lat) -> list:
    """
    将火星坐标系转为百度坐标
    :param lng: pd.Series 经度序列
    :param lat: pd.Series 纬度序列
    :return: list[pd.Series] 经纬度序列数组
    """
    z = np.sqrt(lng * lng + lat * lat) + .00002 * np.sin(lat * constance.X_PI)
    theta = np.arctan2(lat, lng) + .000003 * np.cos(lng * constance.X_PI)
    bd_lng = z * np.cos(theta) + .0065
    bd_lat = z * np.sin(theta) + .006
    return [bd_lng, bd_lat]


def bd09towgs84(lng, lat) -> list:
    """
    将百度坐标系转为wgs84坐标
    :param lng: pd.Series 经度序列
    :param lat: pd.Series 纬度序列
    :return: list[pd.Series] 经纬度序列数组
    """
    if _is_out_of_china(lng, lat):
        return [lng, lat]
    gcjlng, gcjlat = bd09togcj02(lng, lat)
    wgslng, wgslat = gcj02towgs84(gcjlng, gcjlat)
    return [wgslng, wgslat]


def bd09togcj02(lng, lat) -> list:
    """
    将百度坐标系转为火星坐标
    :param lng: pd.Series 经度序列
    :param lat: pd.Series 纬度序列
    :return: list[pd.Series] 经纬度序列数组
    """
    x = lng - .0065
    y = lat - .006
    z = np.sqrt(x * x + y * y) - .00002 * np.sin(y * constance.X_PI)
    theta = np.arctan2(y, x) - .000003 * np.cos(x * constance.X_PI)
    gcj_lng = z * np.cos(theta)
    gcj_lat = z * np.sin(theta)
    return [gcj_lng, gcj_lat]


def lnglattomercator(
        lng,
        lat,
        reference_position: list = (0, 0),
        convert_rate: list = (1, 1),
) -> list:
    """
    将经纬度坐标二维展开为平面坐标
    :param lng: pd.Series 经度坐标序列
    :param lat: pd.Series 纬度坐标序列
    :param reference_position: list[float] 经纬度参照零点坐标，如城市中心或项目中心
    :param convert_rate: list[float] 形变比例
    :return: list[pd.Series] 展开后的二纬坐标，单位为毫米
    """
    x = lng - reference_position[0]
    y = lat - reference_position[1]

    x = x * constance.MERCATOR
    y = np.log(np.tan((90 + y) * constance.PI / 360)) / (constance.PI / 180)
    y = y * constance.MERCATOR

    return [x * convert_rate[0], y * convert_rate[1]]


"""
══════════════════════════════════════════════════════════════════════════════════
"""


def strlocationtofloatlocation(location: pd.Series) -> pd.Series:
    """
    将经纬度序列中字符格式的经纬坐标转为数字列表格式的经纬坐标，用以计算
    :param location: pd.Series of str 如'123.456, 123.456'
    :return: pd.Series of list 如[123.456, 123.456]
    """
    str_locations = location.str.split(',')
    str_locations.astype(list)
    return str_locations.apply(lambda list_: [float(item) for item in list_])


def floatlocationtostrlocation(location: pd.Series) -> pd.Series:
    """
    将将经纬度序列中的经纬坐标转为字符格式的经纬坐标，用以请求
    :param location: pd.Series of list 如[123.456, 123.456]
    :return: pd.Series of str 如'123.456, 123.456'
    """
    return location.apply(lambda cell: ','.join([text for text in map(str, cell)]))


def csvtojson(csv_path: str, json_path: str) -> None:
    """
    将一个 csv 文件转为 json 文件
    :param csv_path: csv 文件路径
    :param json_path: json 文件路径
    :return:
    """
    df = pd.read_csv(csv_path, index_col=0)
    df.to_json(json_path, force_ascii=False)


def csvtogeojson():
    pass


def jsontocsv(json_path, csv_path):
    df = pd.read_json(json_path, encoding='utf-8')
    df.dataframe.reset_index(drop=True, inplace=True)
    df.to_csv(csv_path, encoding='utf_8_sig')


def jsontogeojson(
        json_path: str,
        geojson_path: str,
        feature_type: str = 'Point',
        location_key: str = 'location'
):
    with open(json_path, 'r', encoding='utf-8') as jf:
        data = json.load(jf, encoding='utf-8')

    g_dict = {
        "type": "FeatureCollection",
        "name": 'None',
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        }
    }

    features = list()

    for item in data:
        # item为字符串，格式为'123.456,123.456'
        item_dict = dict()
        item_dict["type"] = "Feature"

        item_dict["geometry"] = dict()
        item_dict["geometry"]['type'] = feature_type
        s_location = item[location_key].split(',')  # 分别提取经纬度
        l_location = [item for item in map(float, s_location)]  # 将值浮点数化
        item_dict["geometry"]['coordinates'] = l_location

        item_dict["properties"] = dict()
        del item[location_key]
        item_dict["properties"].update(item)
        features.append(item_dict)

    g_dict["features"] = features

    with open(geojson_path, 'w', encoding='utf-8') as gf:
        json.dump(g_dict, gf, ensure_ascii=False)


def geojsontojson():
    pass


def geojsontocsv():
    pass
