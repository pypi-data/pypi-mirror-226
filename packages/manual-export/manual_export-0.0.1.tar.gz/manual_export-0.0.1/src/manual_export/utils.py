#!/usr/bin/python3
# -*- coding:utf-8 -*-
import configparser
import logging
import os, sys
import json
import datetime
import re

import psutil

from enums import LtType


def get_file_path(file_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', file_name)

def get_cron(name):
    cron_list = config.get("cron", name).split(" ")
    prefix = list(map(lambda x: None if x == '0' else x, cron_list[:3]))
    suffix = list(map(lambda x: None if x == '-1' else x, cron_list[3:]))
    prefix.extend(suffix)
    return tuple(prefix)

# 获取配置
def get_config():
    config = configparser.RawConfigParser()
    if sys.platform == "win32":
        config.read(get_file_path("config-win.cfg"), encoding="utf-8")
    else:
        config.read(get_file_path("config.cfg"), encoding="utf-8")
    return config


config = get_config()


def in_zone():
    if config.has_option('global', 'zone'):
        return config.getboolean('global', 'zone')
    return False


# 时间日期格式化
def get_time_string_by_pattern(date, pattern):
    time_string = date.strftime(pattern)
    return time_string


# 获取日期
def get_time_date_by_pattern(time_string, pattern):
    date = datetime.datetime.strptime(time_string, pattern)
    return date


def get_retentionpolicy_measurements(re_me_string):
    list = re_me_string.split(".")
    return list[0], list[1]


# 获取文件夹
def get_path_dir(date, dir_path, pattern):
    time_string = get_time_string_by_pattern(date, pattern)
    path = dir_path + time_string + os.sep
    if not os.path.exists(path):
        os.makedirs(path)
    return path


# 获取文件名
def get_file_name(date, pattern, model, *args):
    time_string = get_time_string_by_pattern(date, pattern)
    return model.format(time_string, *args)


def scada_home():
    if sys.platform == "win32":
        return 'D:\\scada'
    return '/home/scada'


def scada_data_dir():
    return os.path.join(scada_home(), 'data')


def scada_log_dir():
    return os.path.join(scada_home(), 'logs')

def scada_starfish_influxdb_dir():
    if(sys.platform == "win32"):
        return os.path.join(scada_home(),'data','starfish','influxdb')
    return os.path.join(scada_home(),'semi','data','DHTFC','starfish','influxdb')

_new_common_config_dir = os.path.join(scada_home(), 'config')


def get_last_time_path(lt_type: LtType = LtType.MysqlScada):
    '''
    type: options are ['scada','ems','influxdb']
    '''

    correct_lasttime_dir = os.path.join(scada_data_dir(), 'starfish')
    lasttime_dir = config.get('path', 'lasttime')
    if os.path.exists(lasttime_dir) and not os.path.exists(correct_lasttime_dir):
        os.makedirs(correct_lasttime_dir, exist_ok=True)
        os.system(f'cp -rf {lasttime_dir} {correct_lasttime_dir}')
    if correct_lasttime_dir != lasttime_dir:
        lasttime_dir = correct_lasttime_dir

    file_path = os.path.join(lasttime_dir, f'{lt_type.value}_lasttime.txt')
    if not os.path.exists(file_path):
        lasttime = datetime.datetime.now() - datetime.timedelta(days=5)
        lasttime = lasttime.strftime('%Y-%m-%d')
        with open(file_path, 'w', encoding='utf-8') as fw:
            fw.write(lasttime)
    return file_path


# 获取最后一次写入时间
def get_last_time(lt_type: LtType = LtType.MysqlScada):
    path = get_last_time_path(lt_type)
    with open(path, mode='r', encoding='utf-8') as f:
        lt = f.read()
        if lt is not None and len(lt):
            return re.sub('\\s+', '', lt)
        return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')


scada_mysql_lasttime_k = 'mysql_lasttime'
ems_mysql_lasttime_k = 'ems_lasttime'
influxdb_day_lasttime_k = 'influxdb_day_lasttime'
influxdb_month_lasttime_k = 'influxdb_month_lasttime'


# 设置最后一次写入时间
def set_last_time(date: str, lt_type: LtType = LtType.MysqlScada):
    path = get_last_time_path(lt_type)
    with open(path, mode='w', encoding='utf-8') as f:
        f.write(date)


def get_farms(only_codes=False):
    path = os.path.join(_new_common_config_dir, 'farm.json')

    farmlist = json.loads(open(path, mode='r', encoding="utf-8").read())
    if only_codes:
        return [farm['farm_code'] for farm in farmlist]
    return farmlist


farm_list = get_farms(True)


def get_turbines(farm_code=None, inner_turbine_name=None):
    path = os.path.join(_new_common_config_dir, 'turbine.json')

    turbine_list = json.loads(open(path, mode='r', encoding="utf-8").read())
    if farm_code:
        turbines = [turbine for turbine in turbine_list if turbine['farm_code'] == farm_code]
        if inner_turbine_name:
            return [turbine for turbine in turbines if turbine['inner_turbine_name'] == inner_turbine_name]
        return turbines
    return turbine_list


def get_turbine_inner_names(farm_code):
    return [turbine['inner_turbine_name'] for turbine in get_turbines(farm_code)]


def get_turbine_type(farm_code, turbine_inner_name):
    turbines = [turbine for turbine in get_turbines(farm_code) if
                turbine['inner_turbine_name'] == turbine_inner_name]
    if turbines:
        return turbines[0]['type_name']
    return turbine_inner_name


def get_turbine_point_version_key(farm_code, turbine_inner_name):
    turbines = [turbine for turbine in get_turbines(farm_code) if
                turbine['inner_turbine_name'] == turbine_inner_name]
    if turbines:
        t = turbines[0]
        return f'{t["point_name"]}:{t["point_version"]}'


def get_points_map():
    path = os.path.join(_new_common_config_dir, 'point.json')
    points_map = json.loads(open(path, mode='r', encoding="utf-8").read())
    return {point_version_key: {point['variable_name']: point['variable_name_old']
                                for point in points
                                if point['variable_name'] and point['variable_name_old']}
            for point_version_key, points in points_map.items()}


def all_processes():
    for p in psutil.process_iter():
        if p.name().lower() == 'python3':
            yield p


def add_prefix_suffix(filename:str, prefix, suffix):
    '''
    :param filename:
    :param prefix:
    :param suffix:
    :return: prefix + filename + suffix
    '''
    return prefix + filename + suffix
if __name__ == '__main__':
    x = get_points_map()
    for v, points in x.items():
        print(v)
        l = len(list(points.values()))
        dl = len(set(list(points.values())))
        print(l, dl, l == dl)

    print(x['SE14125:V1.5.2'])
