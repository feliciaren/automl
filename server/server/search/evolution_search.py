'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-18 22:53:07
@LastEditors: feliciaren
@LastEditTime: 2020-05-20 09:12:45
'''
import numpy as np
import time
import logging
import random

from server.model.study import Study 
from server.model.trials import Trials 
from server.search.basic_search import BasicSearch
from server.search.random_search import RandomSearch
from server.search.static import RandomAlgorithm

__all__ = ['EvolutionSearch']

class EvolutionSearch(BasicSearch):

       
    def _get_next_trial(self,study=None,trials_list = [],number = 1):

        logging.info('EvolutionSearch, need number{}'.format(number))

        assert(study.__class__==Study)
        self.params = study.configuration
        self.study_name = study.name
        self.goal = study.goal
        self.study = study


        self.population_size = 3
        number = 1

        # Use random search if it has less dataset
        completed_trials_list = [trial for trial in trials_list if trial.metric != None ]
        # print(len(completed_trials_list))
        if len(completed_trials_list) < self.population_size:
            randomSearch= RandomSearch()
            return_trials = randomSearch._get_next_trial(self.study, completed_trials_list, number)
            return return_trials
        
        self.population = completed_trials_list

        random.shuffle(self.population)
        if self.population[0].metric < self.population[1].metric:
                self.population[0] = self.population[1]

        suggested_dict = self.population[0].params
        # mutation
        is_rand = {}
        keys = [param["parameterName"] for param in self.params]
        mutation = random.randint(0,len(keys))
        for i in range(len(keys)):
            is_rand[keys[i]] = (i == mutation)
        
        for i in range(len(suggested_dict)):
            if is_rand == False:
                param = self.params[i]
                if param["type"] == "DOUBLE":
                    suggest_value = RandomAlgorithm.get_random_value(
                        param["minValue"], param["maxValue"])

                elif param["type"] == "INTEGER":
                    suggest_value = RandomAlgorithm.get_random_int_value(
                        param["minValue"], param["maxValue"])

                elif param["type"] == "DISCRETE":
                    feasible_point_list = param["feasiblePoints"]
                    suggest_value = RandomAlgorithm.get_random_item_from_list(
                        feasible_point_list)

                elif param["type"] == "CATEGORICAL":
                    feasible_point_list = param["feasiblePoints"]
                    suggest_value = RandomAlgorithm.get_random_item_from_list(
                        feasible_point_list)

                suggested_dict[keys[i]] = suggest_value
        
        new_trial = Trials(study_name = self.study_name,params=suggested_dict,create_time=time.time(),update_time=time.time())

        return [new_trial]


