'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-22 19:36:41
@LastEditors: feliciaren
@LastEditTime: 2020-02-23 14:46:51
'''

import itertools

from server.search.basic_search import BasicSearch
from server.study import Study 
from server.trials import Trials 

class GridSearch(BasicSearch):

    def __init__(self,study = None):


        params = study.configuration
        
        # [['8', '16', '32', '64'], ['sgd', 'adagrad', 'adam', 'ftrl'], ['true', 'false']]
        param_values_list = []
        param_key_list = []
        for param in params:

            # Check param type
            if param["type"] == "DOUBLE" or param["type"] == "INTEGER":
                raise Exception("Grid search does not support DOUBLE and INTEGER")

            param_values_list.append(param["feasiblePoints"])
            param_key_list.append(param["parameterName"])

        self.param_num = len(param_key_list)
        all_combination_value = list(itertools.product(*param_values_list))
        self.all_combination = []

        for value in range(len(all_combination_value)):
            combination = {}
            for j in len(value):
                combination[param_key_list[j]] = value[j]
            self.all_combination.append(combination)
    
    def _get_next_trial(self,trials_list = [],number = 1):
        
        if len(trials_list)<self.param_num:
            trials_list.append(self.all_combination[len(trials_list)])
            return trials_list[-1]
        else:
            return None

    


        




