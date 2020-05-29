'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-05 22:35:43
@LastEditors: feliciaren
@LastEditTime: 2020-05-20 22:26:43
'''

import logging

from server.model.study import Study 
from server.model.trials import Trials 
from server.early_stop.basic_early_stop import BasicEarlyStopAlgorithm

class MedianStop(BasicEarlyStopAlgorithm):
    
    def _should_early_stop(self, study, trials_history,trial_metric):

        assert(study.__class__==Study)

        logging.info('MedianStop, trials history length{}'.format(len(trials_history)))
        
        if len(trials_history) < 3:
            return False
        
        # history_metric = [trial.metric for trial in trials_history]
        

        if study.goal ==  "MINIMIZE":
            trials_history = -1*trials_history
            

        trials_history.sort()

        if trial_metric < trials_history[(len(trials_history)-1)//2]:
            return True
        
        return False