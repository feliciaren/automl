'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-06 17:43:32
@LastEditors: feliciaren
@LastEditTime: 2020-05-06 20:47:54
'''
import enum
__all__ = ['RespType']

class RespType(enum.Enum):
    JSON = 0
    MSGPACK = 1