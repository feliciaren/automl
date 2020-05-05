'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-02 18:48:48
@LastEditors: feliciaren
@LastEditTime: 2020-03-19 09:17:35
'''
import requests 
import json
import os
import sys
from study import Study

basic_url = '0.0.0.0.8686'

__all__=['Worker']

class Worker(object):

    def __init__(self,
                name,
                study = None,
                current_trial = None,
                algorithm = "BayesianOptimization",
                create_time = None,
                update_time = None,
                search = None,
                number = 0):

        self.name = name
        self.study = study
        self.current_trial = current_trial
        self.algorithm = algorithm
        self.create_time = create_time
        self.update_time = update_time
        self.search = search
        self.study = None
        self.number = number
    
    def _early_stop(self,):
        pass
        
    
    def _get_next_step(self,trial_list,number):

        if self.study == None:
            raise "Wrong Study Type"
        
        request = self.study._to_dict()
        if self.number == 0:
            request['trial_list'] = []
        
        next_trial = requests.get(basic_url + requests)

        return next_trial
        


    
    @classmethod
    def fromjson(self,json_file):
        self.study = Study(json_file)

        