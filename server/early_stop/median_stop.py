'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-05 22:35:43
@LastEditors: feliciaren
@LastEditTime: 2020-05-06 00:07:43
'''

from basic_early_stop import AbstractEarlyStopAlgorithm

class MedianStop(AbstractEarlyStopAlgorithm):
    def _should_early_stop(self,study=None,self.trials_history,trial_metric):
        
        if len(self.trials_history) < 3:
            return False
        
        history_metric = [trial.metric for trial in self.trials_history]
        

        if study.goal =  "MINIMIZE":
            history_metric = -1*history_metric
            

        history_metric.sort()

        if trial_metric[-1] < history_metric[(len(history_metric)-1)//2]:
            return True
        
        return False