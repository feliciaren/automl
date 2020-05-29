'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-02 18:48:48
@LastEditors: feliciaren
@LastEditTime: 2020-05-29 18:37:04
'''
__all__ = ['Study']

import json
import uuid
import time

from server.model.trials import Trials

class Study(object):
    
    def __init__(self,
                name,
                configuration,
                algorithm = "BayesianOptimization",
                goal = None,
                earlystop = None,
                trials_list = None,
                number = None,
                create_time = None,
                update_time = None):

        self.name = name
        self.configuration = configuration
        self.algorithm = algorithm
        self.goal = goal
        self.create_time = create_time
        self.update_time = update_time
        self.earlystop = earlystop
        self.trials_list = trials_list
        self.number = number

    def _to_json(self):
        dic = self._to_dict()
        with open(self.name,'w',encoding='utf-8') as f:
            json.dump(f,dic,indent=4)

    def _info(self):
        print("================{}_Configuration================".format(self.name))
        print("Create Time: {}, Update Time:{}".format(time.asctime(time.localtime(self.create_time)),time.asctime(time.localtime(self.update_time))))
        print("Goal:{}".format(self.goal))
        print("Feasible Space:")
        for key in self.configuration:
            print("{}: {}".format(key,self.configuration[key]))
        
    
    def _to_dict(self):
        dic = {}
        dic['name'] = self.name
        dic['params'] = self.configuration
        dic['create_time'] = self.create_time
        dic['update_time'] = self.update_time
        dic['goal'] = self.goal
        return dic


    @classmethod
    def _from_dict(self,dic):
        # with open(json_file,'r',encoding='utf-8') as f:
        #     dic = json.load(f)

        try:
            assert('name' in dic)
            name = dic.pop('name') + '_' + str(uuid.uuid3(uuid.NAMESPACE_DNS,str(time.time())))
        except AssertionError:
            name = ' _' + str(uuid.uuid3(uuid.NAMESPACE_DNS,str(time.time())))

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

        try:
            assert('earlystop' in dic)
            earlystop = dic.pop('earlystop')
            try:
                assert('trials_history' in earlystop)
            except AssertionError:
                earlystop['trials_history'] = []
            try:
                assert('name' in earlystop)
            except AssertionError:
                earlystop['name'] = "MedianStop"
            try:
                assert('trial_metric' in earlystop)
            except AssertionError:
                earlystop['trial_metric'] = None
        except AssertionError:
            earlystop = None


        try:
            assert('number' in dic)
            number = dic.pop('number')
        except AssertionError:
            number = None


        try:
            assert('trials_list' in dic)
            json_list = dic.pop('trials_list')
            trials_list = []
            for trial_dic in json_list:
                trial = Trials._from_dict(trial_dic)
                trials_list.append(trial)
        except AssertionError:
            trials_list = None
        
        return Study(name = name,configuration = dic['params'],algorithm = algorithm, goal = goal,earlystop=earlystop,trials_list=trials_list,number = number,create_time = time.time(),update_time = time.time())
    
    @classmethod
    def _from_json(self,json_file):
        with open(json_file,'r',encoding='utf-8') as f:
            dic = json.load(f)

        try:
            assert('name' in dic)
            name = dic.pop('name') + '_' + str(uuid.uuid3(uuid.NAMESPACE_DNS,str(time.time())))
        except AssertionError:
            name = ' _' + str(uuid.uuid3(uuid.NAMESPACE_DNS,str(time.time())))

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


        try:
            assert('number' in dic)
            number = dic.pop('number')
        except AssertionError:
            number = None

        try:
            assert('trials_list' in dic)
            json_list = dic.pop('trials_list')
            trials_list = []
            for trial_dic in json_list:
                trial = Trials._from_dict(trial_dic)
                trials_list.append(trial)
        except AssertionError:
            trials_list = None

        try:
            assert('earlystop' in dic)
            earlystop = dic.pop('earlystop')
            try:
                assert('trials_history' in earlystop)
            except AssertionError:
                earlystop['trials_history'] = []
            try:
                assert('name' in earlystop)
            except AssertionError:
                earlystop['name'] = "MedianStop"
            try:
                assert('trial_metric' in earlystop)
            except AssertionError:
                earlystop['trial_metric'] = None
        except AssertionError:
            earlystop = None
        
        return Study(name = name,configuration = dic['params'],algorithm = algorithm, goal = goal,earlystop=earlystop,trials_list=trials_list,number = number,create_time = time.time(),update_time = time.time())