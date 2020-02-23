'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-23 10:25:07
@LastEditors: feliciaren
@LastEditTime: 2020-02-23 14:43:11
'''
import abc

class BasicSearch(object):
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def _get_next_trial(self, study = None, trials_list = [], number = 1):

      '''
      Args:
        study: The study object.
        trials_list: The all trials of this study.
        number: The number of trial to return. 
      Returns:
        The array of trial objects.

      The study's study_configuration is like this.
      {
            "goal": "MAXIMIZE",
            "maxTrials": 5,
            "maxParallelTrials": 1,
            "params": [
                {
                    "parameterName": "hidden1",
                    "type": "INTEGER",
                    "minValue": 40,
                    "maxValue": 400,
                    "scalingType": "LINEAR"
                }
            ]
        }
      
      The trial's parameter_values_json should be like this.
      {
            "hidden1": 40
      }
      
      '''

      raise NotImplementedError