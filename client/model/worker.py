'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-02 18:48:48
@LastEditors: feliciaren
@LastEditTime: 2020-05-29 10:27:58
'''

import json
import os
import asyncio
import time
import copy
import requests
from client.model.study import Study
from client.model.trials import Trials


__all__=['Worker']

class Worker(object):

    def __init__(self,
                name="worker",
                study = None,
                create_time = None,
                update_time = None):

        self.name = name
        self.study = study
        self.create_time = create_time
        self.update_time = update_time

    
    def _should_trial_stop(self,url,trial_history,trial_metric,algorithm="MedianStop"):
        earlystop = {}
        earlystop['name'] = algorithm
        earlystop['trials_history'] = trial_history
        earlystop['trials_metric'] = trial_metric
        self.study.earlystop = earlystop
        request_json = self.study._to_dict()    
        response = requests.post(url,data=request_json)
        return response.json()
      

    def _add_measurement_to_trial(self,trial_metric,trial):
        trial.status = "Pending"
        trial.metric = trial_metric
    
    def _complete_trial(self,trial_metric,trial):
        trial.status = "Complete"
        trial.metric = trial_metric
    
    def _get_next_trials(self,url,trials_list,number):
            
        request_json = self.study._to_dict()
        request_json['trials_list'] = trials_list
        request_json['number'] = number
        response = requests.post(url,data=request_json)
        return response.json()
    
    def _get_study_name(self):
        return self.study.name
    
    def _load_json(self,json):
        self.study = Study._from_dict(json)
        self.name = str(self.study.name) + '_Worker'
        self.algorithm = self.study.algorithm
        self.create_time = time.time()
        self.update_time = time.time()
    
    @classmethod
    def _from_json(self,json_file):

        study = Study._from_dict(json_file)
        return Worker(str(study.name) + '_Worker',study = study,create_time=time.time(),update_time=time.time())

