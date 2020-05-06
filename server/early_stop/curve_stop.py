'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-05 22:36:04
@LastEditors: feliciaren
@LastEditTime: 2020-05-06 00:16:31
'''
from basic_early_stop import AbstractEarlyStopAlgorithm
from curve_model import *

threahold = 0.95

class CurveStop(AbstractEarlyStopAlgorithm):

    def _should_early_stop(self,study=None,self.trials_history,trial_metric):

        if len(self.trials_history) < 3:
            return False
        
        history_metric = [trial.metric for trial in self.trials_history]

        standard_metric = history_metric * threahold

        curvemodel = CurveModel(study.earlystop['target_pos'])
        predict_y = curvemodel.predict(history_metric)

        if self.study.goal = "MINIMIZE":
            if predict_y <= standard_metric :
                return True
        
        if self.study.goal = "MAXIMIZE" :
            if predict_y >= standard_metric :
                return True
        
        return False
        

