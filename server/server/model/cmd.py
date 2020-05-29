'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-03-19 07:59:30
@LastEditors: feliciaren
@LastEditTime: 2020-05-06 21:15:20
'''

import argparse

import asyncio
import aiohttp.web


from server.model.worker import Worker
from server.model.http_handler import HTTPHandler
from server.model.globals import RespType


parser = argparse.ArgumentParser(description='A simple AutoML serving application by using PyTorch and aiohttp.')


parser.add_argument('--unix-socks-path', type=str, default='',
                    help='Unix socks file path')
parser.add_argument('--port', type=int, default=8686,
                    help='http port')
parser.add_argument('--host', type=str, default='0.0.0.0',
                    help='http host')
parser.add_argument('--default-response-type', type=str, default='json',
                    help='The default response type if request does not specify. Should in (msgpack, json).')                   


args = parser.parse_args()
__all__ = ['entry_point']


def _str2bool(s: str) -> bool:
    return s.lower() in ['t', 'true', 'on', '1']

def entry_point():
    print(args)
    path = args.unix_socks_path
    try:
        port = args.port
    except (TypeError, ValueError):
        port = None
    host = args.host

    model = Worker()

    handler = HTTPHandler(model=model,
                          default_response_type=RespType[
                        args.default_response_type.upper()])
    app = aiohttp.web.Application()
    app.add_routes([aiohttp.web.post('/', handler.post)])

    app.on_startup.append(model.startup)

    # aiohttp.web.run_app(app, port=port, path=path, host=host)
    aiohttp.web.run_app(app, port=port, host=host)
