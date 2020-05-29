'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-23 21:05:21
@LastEditors: feliciaren
@LastEditTime: 2020-05-17 23:48:49
'''
__all__ = ['RandomSearch']
import json
import random
import time
import logging 

from server.model.study import Study
from server.model.trials import Trials
from server.search.basic_search import BasicSearch
from server.search.static import RandomAlgorithm


class RandomSearch(BasicSearch):
	
  def _get_next_trial(self, study, trials_list=[], number=1):
    """
    Get the new suggested trials with random search.
    """
    logging.info('RandomSearch, need number{}'.format(number))
    return_list = []
    params = study.configuration
    study_name = study.name

    for i in range(number):
      parameter_values_json = {}

      for param in params:

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

        parameter_values_json[param["parameterName"]] = suggest_value

      new_trial = Trials(study_name = study_name,params=parameter_values_json,create_time=time.time(),update_time=time.time())
      return_list.append(new_trial)
      # trials_list.append(new_trial)

    return return_list
