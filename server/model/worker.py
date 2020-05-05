'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-02 18:48:48
@LastEditors: feliciaren
@LastEditTime: 2020-03-19 09:08:01
'''

import json
import os
import asyncio
from model.study import Study
from search.bayesian_optimization import BayesianOptimization
from search.random_search import RandomSearch
from search.grid_search import GridSearch

__all__=['Worker']

class Worker(object):

    def __init__(self,
                name,
                study = None,
                current_trial = None,
                algorithm = "BayesianOptimization",
                create_time = None,
                update_time = None,
                search = None):

        self.name = name
        self.study = study
        self.current_trial = current_trial
        self.algorithm = algorithm
        self.create_time = create_time
        self.update_time = update_time
        self.search = search
        self.study = None
    
    def _early_stop(self,):
        pass
        
    
    async def _get_next_step(self):

        if self.search == None:
            raise "Wrong Search Type"
        self.current_trial = self.search._get_next_trial(trials_list = self.study.configuration['trial_list'],number = self.study.configuration['number'])
        self.current_trial._info()
        return self.current_trial

    
    @classmethod
    def fromjson(self,json_file):

        self.study = Study(json_file)
        if self.study.algorithm == "GridSearch":
            self.search = GridSearch(self.study)
        elif self.study.algorithm == "RandomSeach":
            self.search = RandomSearch(self.study)     
        elif self.study.algorithm == "BayesianOptimization":
            self.search = BayesianOptimization(self.study)
        

