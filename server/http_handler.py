'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-03-19 07:46:11
@LastEditors: feliciaren
@LastEditTime: 2020-03-19 08:49:04
'''
from model.worker import Worker
from model.globals import RespType
import msgpack
import aiohttp.web

__all__ = ['HTTPHandler']


class HTTPHandler:
    def __init__(self,
                model: Server,
                default_response_type: RespType = RespType.JSON):
        self.model = model
        self._default_response_type = default_response_type
    
    async def post(self, req):
        request = await req.json()
        # request = request['q']
        print(request)
        self._model = self.model.fromjson(request)
        next_param = await self._model.predict(request)
        rsp_type = request.get("response_type", None)

        if isinstance(rsp_type, str):
            rsp_type = RespType[rsp_type.upper()]
        else:
            rsp_type = self._default_response_type
        
        if rsp_type == RespType.JSON:
            return aiohttp.web.json_response(next_param)
        elif rsp_type == RespType.MSGPACK:
            rsp = aiohttp.web.Response(
                headers={'Content-Type': 'application/x-msgpack'},
                status=200,
                body=msgpack.packb(next_param),
                reason='OK')
            return rsp