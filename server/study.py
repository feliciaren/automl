'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-02 18:48:48
@LastEditors: feliciaren
@LastEditTime: 2020-02-23 23:24:12
'''
__all__ = ['Study']
import json
import uuid
import time
class Study(object):
    
    def __init__(self,
                name,
                configuration,
                algorithm = "BayesianOptimization",
                goal = None,
                create_time = None,
                update_time = None):

        self.name = name
        self.configuration = configuration
        self.algorithm = algorithm
        self.goal = goal
        self.create_time = create_time
        self.update_time = update_time

    def _to_json(self):
        dic = self._to_dict()
        with open(self.name,'w',encoding='utf-8') as f:
            json.dump(f,dic,indent=4)

    def _info(self):
        print("================{}_Configuration================".format(self.name))
        print("Create Time: {}, Update Time:{}".format(time.asctime(time.localtime(self.create_time)),time.asctime(time.localtime(self.update_time))))
        print("Goal:{}".format(self.goal))
        print("Feasible Space:")
        for key in self.configuaration:
            print("{}: {}".format(key,self.configuaration[key]))
    
    def _to_dict(self):
        dic = {}
        dic['name'] = self.name
        dic['configuaration'] = self.configuaration
        dic['create_time'] = self.create_time
        dic['update_time'] = self.update_time
        dic['goal'] = self.goal
        return dic

    @classmethod
    def fromjson(self,json_file):
        with open(json_file,'r',encoding='utf-8') as f:
            dic = json.load(f)

        try:
            assert('name' in dic)
            name = dic.pop('name') + uuid.uuid3(uuid.NAMESPACE_DNS,dic['name'])
        except AssertionError:
            name = uuid.uuid3(uuid.NAMESPACE_DNS,'')

        try:
            assert('goal' in dic)
            goal = dic.pop('goal')
        except AssertionError:
            goal = None

        try:
            assert('algorithm' in dic)
            algorithm = dic.pop('algorithm')
        except AssertionError:
            algorithm = "BayesianOptimization"
        
        return Study(name = name,configuration = dic['params'],algorithm = algorithm, goal = goal,create_time = time.time(),update_time = time.time())