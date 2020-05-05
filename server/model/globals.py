'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-03-19 07:50:47
@LastEditors: feliciaren
@LastEditTime: 2020-03-19 07:51:05
'''
import enum


__all__ = ['RespType']


class RespType(enum.Enum):
    JSON = 0
    MSGPACK = 1