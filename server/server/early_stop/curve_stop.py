'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-05 22:36:04
@LastEditors: feliciaren
@LastEditTime: 2020-05-20 22:26:57
'''
from server.early_stop.basic_early_stop import BasicEarlyStopAlgorithm
from server.early_stop.curve_model import *



class CurveStop(BasicEarlyStopAlgorithm):
    
    def _should_early_stop(self, study, trials_history,trial_metric):

        if len(trials_history) < study.earlystop['target_pos']//2:
            return False
        
        threahold = 0.95

        # history_metric = [trial.metric for trial in trials_history if trial.metric != None] 

        curvemodel = CurveModel(study.earlystop['target_pos'])
        predict_y = curvemodel.predict(trials_history)

        if predict_y == None:
            return False

        if study.goal == "MINIMIZE":
            standard_metric = max(trials_history) * threahold
            if predict_y > standard_metric :
                return True
        
        if study.goal == "MAXIMIZE" :
            standard_metric = min(trials_history) * threahold
            if predict_y < standard_metric :
                return True
        
        return False
        

