'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-23 10:25:07
@LastEditors: feliciaren
@LastEditTime: 2020-05-05 20:54:26
'''
import abc
__all__ = ['BasicSearch']
class BasicSearch(object):
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def _get_next_trial(self,study=None):

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

      pass