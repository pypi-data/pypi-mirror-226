# -*- coding: utf-8 -*-
# Created By Shing At 2022/9/15

import enum


class LtType(enum.Enum):
    '''
    lasttime 类型
    '''
    MysqlScada = 'mysql_scada'
    MysqlEms = 'mysql_ems'
    Influxdb = 'influxdb'
    MysqlEvent = 'mysql_event'
    InfluxdbEms = 'influxdb-ems'

if __name__ == '__main__':
    print(LtType.MysqlScada.value)
