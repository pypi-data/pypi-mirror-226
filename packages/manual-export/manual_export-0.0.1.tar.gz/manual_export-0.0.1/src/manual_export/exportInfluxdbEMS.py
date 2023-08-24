#!/usr/bin/python3
# -*- coding:utf-8 -*-
import datetime
import dis
import math
import os.path
import time
from multiprocessing import Pool

import pandas as pd
from influxdb import InfluxDBClient

import utils
from utils import *
import logging

prefix = ""
suffix = ""
lasttime_pattern = "%Y-%m-%d"
influx_databases = eval(config.get('influxdb', 'databases'))
influx_dir_path = config.get('path', 'influxdb')

# 只是创建了对象，并没有建立连接。influxdb的增删改查，用的是http协议
influxdb_client = InfluxDBClient(host=config.get('influxdb', 'host'),
                                 port=config.get('influxdb', 'port'),
                                 username=config.get('influxdb', 'username'),
                                 password=config.get('influxdb', 'password'),
                                 timeout=10000)
inner_turbine_name_start = None
# waiting util influxdb started
now = time.time()
while True:
    try:
        logging.info('waiting influxdb server active')
        influxdb_client.query('show databases')
        logging.info('influxdb server connected')
        break
    except Exception as e:
        delta = time.time() - now
        if delta > 3 * 60:
            time.sleep(5)
        elif delta > 5 * 60:
            time.sleep(10)
        elif delta > 10 * 60:
            time.sleep(60)
        else:
            time.sleep(1)


class ExportInfluxdbEMS:

    def export(self, start: datetime.datetime = None, end: datetime.datetime = None, turbine=None):
        if start and end and start == end:
            return

        with Pool(1) as tp:
            t = time.time()
            ss = start
            ee = end

            if start is None or end is None:
                start = get_time_date_by_pattern(get_last_time(LtType.InfluxdbEms), lasttime_pattern)
                end = start + datetime.timedelta(days=1)
            min_duration = datetime.timedelta(days=1)
            while end - start >= min_duration:
                self._export_day(tp, start, start + min_duration, turbine)
                start += min_duration
            if end > start:
                self._export_day(tp, start, end, turbine)

            logging.info(
                f'export influxdb data,from {ss} to {ee},cost:{time.time() - t}')

            tp.close()
            tp.join()

            if config.getint('log', 'level') == 10:
                from utils import all_processes
                for p in all_processes():
                    logging.debug(f'{p.pid}, {p.cmdline()}, {p.memory_full_info()}')

    def _export_day(self, tp, start_time, end_time, turbine):
        t = time.time()
        ss = start_time
        ee = end_time
        try:
            logging.info(f'开始备份influxdb:{start_time},{end_time}')
            self._export_day_core(tp, start_time, end_time, turbine)
            logging.info(f'exec influx day data complement,date is : {str(start_time)} - {str(end_time)}')
        except Exception as e:
            logging.exception(e)
        finally:
            logging.info(f'导出influxdb数据，{ss},{ee}，cost:{time.time() - t} ')

    def _export_day_core(self, tp, start_time, end_time, turbine):
        progress_info = {}
        for datebase in influx_databases:
            influxdb_client.switch_database(datebase)
            # 带风机属性的表
            turbine_measurements = eval(config.get('influxdb', datebase + ".turbine.measurements"))
            if isinstance(turbine_measurements, list) and len(turbine_measurements) > 0:
                # for farm in farm_list:
                turbines = get_turbine_inner_names(datebase)
                global inner_turbine_name_start
                inner_turbine_name_start = turbines[0]
                count = 0
                cnt = 0  # 方便快速测试 风机数量有30个
                for turbine_id in turbines:
                    cnt += 1
                    # if(cnt > 1):
                    #     break
                    current_id = turbine_id.zfill(3)
                    command_inner_name_lists = []
                    if turbine is not None:
                        command_inner_name_lists.append(turbine)
                    if len(command_inner_name_lists) != 0:
                        if current_id not in command_inner_name_lists:
                            continue
                    for measurement in turbine_measurements:
                        # 拆分measurement获取存储策略和表名
                        retentionpolicy, measure = get_retentionpolicy_measurements(measurement)
                        self.export_data_in_datetime_range(tp, start_time, end_time, datebase, retentionpolicy,
                                                           measure,
                                                           current_id)
                    count += 1
                    progress_info["rate"] = count / len(turbines)
                    logging.info("当前进度： {:.2f} %".format(progress_info["rate"] * 100))

            # 不带风机属性的表
            measurements = eval(config.get('influxdb', datebase + ".measurements"))
            if isinstance(measurements, list) and len(measurements) > 0:
                for measurement in measurements:
                    # 拆分measurement获取存储策略和表名
                    retentionpolicy, measure = get_retentionpolicy_measurements(measurement)
                    self.export_data_in_datetime_range(tp, start_time, end_time, datebase, retentionpolicy, measure)

    def export_data_in_datetime_range(self, tp, start_datetime, end_datetime, database, retention_policy,
                                      measurement,
                                      turbine=None, gzip=True):
        df_list = []
        no_data_time_records = []
        l_start_datetime = start_datetime
        l_end_datetime = start_datetime
        while l_start_datetime < end_datetime and l_end_datetime <= end_datetime:
            l_end_datetime = l_start_datetime + datetime.timedelta(hours=8)
            # logging.info(l_start_datetime)
            # logging.info(l_end_datetime)
            # logging.info("=======================")
            dir_name = get_path_dir(date=l_start_datetime, dir_path=influx_dir_path, pattern="%Y-%m-%d")
            time_string = get_time_string_by_pattern(l_start_datetime, "%Y-%m-%d")
            # 时间日期格式化2018-07-16T10:00:00Z
            start = get_time_string_by_pattern(l_start_datetime - datetime.timedelta(hours=8), "%Y-%m-%dT%H:%M:%SZ")
            end = get_time_string_by_pattern(
                (end_datetime if l_end_datetime > end_datetime else l_end_datetime) - datetime.timedelta(hours=8),
                "%Y-%m-%dT%H:%M:%SZ")
            query = f"select * from \"{database}\".\"{retention_policy}\".\"{measurement}\" " \
                    f"where time >= '{start}' and time < '{end}';"
            logStr = f'{database} -- {retention_policy} -- {measurement} -- {l_start_datetime} -->> {l_end_datetime}'
            if measurement == 'turbine_message_db':
                query = f"select * from \"{database}\".\"{retention_policy}\".\"{measurement}\" " \
                        f"where turbine_name = '{turbine}' and time >= '{start}' and time < '{end}';"
                logStr = f'{database} -- {retention_policy} -- {measurement} -- {turbine} -- {l_start_datetime} -->> {l_end_datetime}'
            # logging.info(logStr)
            t = time.time()
            df = pd.DataFrame(influxdb_client.query(query).get_points())
            if measurement == "turbine_message_db":
                json_file = os.path.join(utils._new_common_config_dir, 'rp_7d-turbine_message_db.json')
                with open(json_file, 'r', encoding='utf-8') as f:
                    field_mapping = json.load(f)
                # # 获取DataFrame的列集合A
                # set_A = set(df.columns)
                # # 获取field_mapping字典的键集合B
                # set_B = set(field_mapping.keys())
                # 找出A中有B没有的元素
                # elements_only_in_A = set_A - set_B
                # logging.info(elements_only_in_A)
                df = df.rename(columns=field_mapping)
            logging.info(f'''exec {query},cost:{time.time() - t}s''')
            # logging.info(query)
            df_columns = [c for c in df.columns if not re.match('^[-]?\\d+[.]?\\d*$', c)]
            df = df[df_columns]
            if len(df):
                df_list.append(df)
                logging.debug(
                    f'load influxdb data:{get_file_name_prefix(database, measurement, turbine)},from {datePattern(l_start_datetime)} to {datePattern(l_end_datetime)} success')
            else:
                no_data_time_records.append(
                    (l_start_datetime, end_datetime if l_end_datetime > end_datetime else l_end_datetime))

            l_start_datetime = l_end_datetime

        index = len(no_data_time_records) - 1
        while index > 0:
            cur = no_data_time_records[index]
            pre = no_data_time_records[index - 1]
            if pre[1] >= cur[0]:
                no_data_time_records[index - 1] = (pre[0], cur[1])
                del no_data_time_records[index]
            index -= 1
        if no_data_time_records:
            for x in no_data_time_records:
                logging.warning(
                    f'influxdb no data: {database}.{retention_policy}.{turbine}.{measurement} in {x[0]},{x[1]}')

        if df_list:
            file_name = generate_turbine_filename(database, turbine, measurement)
            savedir = os.path.join(scada_starfish_influxdb_dir(), time_string)
            if not os.path.exists(savedir):
                os.makedirs(savedir)
            global prefix, suffix
            file_name = add_prefix_suffix(file_name.split(".")[0], prefix, suffix) + '.' + file_name.split(".")[1]
            file_path = os.path.join(savedir, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)

            merge_df = pd.concat(df_list, ignore_index=True)
            merge_df["time"] = pd.to_datetime(merge_df["time"]).dt.tz_localize(None)
            merge_df["time"] = merge_df["time"] + datetime.timedelta(hours=8)
            merge_df = merge_df.sort_values(by=['time'])
            with open(file_path, 'wb') as f:
                merge_df.to_parquet(f, engine='pyarrow', use_deprecated_int96_timestamps=True, index=None)
            logging.info(f'merge files to {file_path} completed')

    def export_data_and_aggregate_config_gridReturn(self, start: datetime.datetime = None,
                                                    end: datetime.datetime = None, updateTimeFlag=True):

        '''
        Args:
            start: 开始时间
            end: 结束时间
            updateTimeFlag: 是否更新 lasttime
            manualFlag: 是否是手动触发  如果是手动触发 在数据落盘时加上后缀 manual_start_end
        Returns:
        '''
        # start_time = get_time_date_by_pattern(get_last_time(LtType.InfluxdbEms), lasttime_pattern)
        # last_time = start_time + datetime.timedelta(days=1)
        # time_string = get_time_string_by_pattern(last_time, lasttime_pattern)

        # if start is not None and end is not None:
        #     logging.info(str(start) + '----->' + str(end))
        #     start_time = start
        #     last_time = end
        # logging.info("数据备份中....")
        self.export(start, end)
        aggregate_config_gridReturn(start.date(), 'config', 'gridReturn')
        # logging.info("数据备份完成....")
        # if updateTimeFlag:
        #     set_last_time(time_string, LtType.InfluxdbEms)
        #     logging.info(f"时间更新完成....,当前last_time的为{time_string}")


def get_file_name_prefix(database, measurement, turbine=None):
    if turbine:
        return f'{database}_{turbine}_{measurement}'
    else:
        return f'{database}_{measurement}'


# def generate_turbine_filename(farm_code, inner_turbine_name, measurement, datestr):
#     if inner_turbine_name:
#         turbine_filename = f"{farm_code}_{inner_turbine_name}_{datestr}_{measurement}.parquet"
#         if measurement == 'turbine_message_db':
#             inner_turbine_name = str(int(inner_turbine_name) - int(inner_turbine_name_start) + 1).zfill(3)
#             turbine_filename = f"{farm_code}_{inner_turbine_name}_{datestr}_{measurement}.parquet"
#         return turbine_filename
#     return f"{farm_code}_{datestr}_{measurement}.parquet"
def generate_turbine_filename(farm_code, inner_turbine_name, measurement):
    if inner_turbine_name:
        turbine_filename = f"{farm_code}_{inner_turbine_name}_{measurement}.parquet"
        if measurement == 'turbine_message_db':
            inner_turbine_name = str(int(inner_turbine_name) - int(inner_turbine_name_start) + 1).zfill(3)
            turbine_filename = f"{farm_code}_{inner_turbine_name}_{measurement}.parquet"
        return turbine_filename
    return f"{farm_code}_{measurement}.parquet"


def datePattern(dt, pattern='%Y%m%d%H%M%S'):
    return dt.strftime(pattern)


def aggregate_config_gridReturn(date: datetime.datetime, file1, file2):
    '''
    Args:
        date: 要聚合的日期 例如 datetime.datetime(year=2022, month=9, day=18)
        file1: 要聚合的表名1 config
        file2: 要聚合的表名2 gridReturn
    Returns:
        生成文件路径  读取两个文件到内存
        聚合文件 再次落盘  同时打印相关日志
    '''
    timeStr = datePattern(date, '%Y%m%d')
    pathStr = datePattern(date, '%Y-%m-%d')
    farms = get_farms(True)
    for farm in farms:
        global prefix, suffix
        fileName1 = farm + '_' + file1
        fileName2 = farm + '_' + file2
        fileName1 = add_prefix_suffix(fileName1, prefix, suffix) + '.parquet'
        fileName2 = add_prefix_suffix(fileName2, prefix, suffix) + '.parquet'
        filePath1 = os.path.join(scada_starfish_influxdb_dir(), pathStr, fileName1)
        filePath2 = os.path.join(scada_starfish_influxdb_dir(), pathStr, fileName2)
        fileMerged = farm + '_ems_log_'
        fileMerged = add_prefix_suffix(fileMerged, prefix, suffix) + '.parquet'
        file_path = os.path.join(scada_starfish_influxdb_dir(), pathStr, fileMerged)
        if not existFile(filePath1):
            return False
        if not existFile(filePath2):
            return False
        merge_parquet(file_path, filePath1, filePath2)
    return True


def existFile(file):
    flag = None
    if not os.path.exists(file):
        logging.warning(file + "  文件不存在，请检查influxdb数据库")
        flag = False
    else:
        flag = True
    return flag


def merge_parquet(file_path, file1, file2):
    # 读取parquet文件
    df1 = pd.read_parquet(file1)
    df2 = pd.read_parquet(file2)
    json_file1 = os.path.join(utils._new_common_config_dir, 'rp_7d-config.json')
    with open(json_file1, 'r', encoding='utf-8') as f:
        field_mapping1 = json.load(f)
    df1 = df1.rename(columns=field_mapping1)
    json_file2 = os.path.join(utils._new_common_config_dir, 'rp_ems_60d-gridReturn.json')
    with open(json_file2, 'r', encoding='utf-8') as f:
        field_mapping2 = json.load(f)
    df2 = df2.rename(columns=field_mapping2)
    df1['time'] = df1['time'].dt.floor('s')
    df2['time'] = df2['time'].dt.floor('s')
    df1 = df1.drop_duplicates(subset='time', keep='first')
    df2 = df2.drop_duplicates(subset='time', keep='first')
    # 合并两个数据框
    merge_df = pd.merge(df1, df2, on='time', how='outer')
    # merge_df["time"] = pd.to_datetime(merge_df["time"]).dt.tz_localize(None)
    # merge_df["time"] = merge_df["time"] + datetime.timedelta(hours=8)
    merge_df = merge_df.sort_values(by=['time'])
    with open(file_path, 'wb') as f:
        merge_df.to_parquet(f, engine='pyarrow', use_deprecated_int96_timestamps=True, index=None)
    logging.info(f'merge files to {file_path} completed')


def manual_save_emsInfluxdb_tillnow(start_time):
    # 手动触发 能管数据落盘的接口
    now_time = datetime.datetime.now()
    today = datetime.date.today()
    today = datetime.datetime(today.year, today.month, today.day)
    global prefix, suffix
    suffix = "_manual_" + get_time_string_by_pattern(start_time,
                                                     "%Y-%m-%d_%H-%M-%S") + "_" + get_time_string_by_pattern(now_time,
                                                                                                             "%Y-%m-%d_%H-%M-%S")
    start_time = datetime.datetime(start_time.year, start_time.month, start_time.day)
    if start_time < today:
        yesterday = today - datetime.timedelta(days=1)
        ExportInfluxdbEMS().export_data_and_aggregate_config_gridReturn(yesterday, today, updateTimeFlag=False)
    #  昨天的数据已经备份好 只用备份今天的数据即可 所以不用更新日期
    ExportInfluxdbEMS().export_data_and_aggregate_config_gridReturn(today, now_time, updateTimeFlag=False)
    prefix = ""
    suffix = ""


def init_influxdb_lasttime():
    # 获取init_influxdb_lasttime.txt 地址  初始化日期为今天
    lasttimefilepath = get_last_time_path(lt_type=LtType.InfluxdbEms)
    # 获取昨天的日期
    # today = datetime.date.today() - datetime.timedelta(days=1)
    today = datetime.date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    # 打开文件并更新内容
    with open(lasttimefilepath, "w") as file:
        file.write(formatted_date)
    logging.info(f'last_time更新为 {formatted_date}')

def get_influxdb_lasttime():
    # 获取init_influxdb_lasttime.txt 地址  初始化日期为今天

    # start_time = datetime.date.today()
    start_time = datetime.date.today() - datetime.timedelta(days=1)
    return start_time


if __name__ == '__main__':
    # s = datetime.datetime(year=2023, month=8, day=15)
    # e = datetime.datetime(year=2023, month=8, day=16)
    # ExportInfluxdbEMS().export(s, e)
    # aggregate_config_gridReturn(s, 'config', 'gridReturn')
    pass

