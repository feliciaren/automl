'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-22 19:36:41
@LastEditors: feliciaren
@LastEditTime: 2020-05-05 20:55:07
'''


__all__ = ['GridSearch']
import itertools
import time



from .basic_search import BasicSearch
from server.model.study import Study 
from server.model.trials import Trials 

class GridSearch(BasicSearch):

    def _get_next_trial(self,study = None,trials_list = [],number = 1):

        assert(study.__class__==Study)
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
        for value in all_combination_value:
            combination = {}
            value = list(value)
            for j in range(len(value)):
                combination[param_key_list[j]] = value[j]
            self.all_combination.append(combination)
        self.combination_num = len(self.all_combination)
        self.study_name = study.name


        return_list = []
        # if len(trials_list)+ number <= self.combination_num:
        for i in range(number):
            idex = len(trials_list) % len(self.all_combination)
            new_trial = Trials(study_name = self.study_name,params=self.all_combination[idex],create_time=time.time(),update_time=time.time())
            trials_list.append(new_trial)
            return_list.append(new_trial)
            # return trials_list[-1]
        return return_list
            

    


        




