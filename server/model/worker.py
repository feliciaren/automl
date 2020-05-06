'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-02 18:48:48
@LastEditors: feliciaren
@LastEditTime: 2020-05-05 23:39:50
'''

import json
import os
import asyncio
import time
import copy

from server.model.study import Study
from server.search.bayesian_optimization import BayesianOptimization
from server.search.random_search import RandomSearch
from server.search.grid_search import GridSearch
from server.search.cmaes import CmaesAlgorithm
from server.search.simulate_anneal import SimulateAnnealAlgorithm
from server.search.tpe import TpeAlgorithm

__all__=['Worker']

class Worker(object):

    def __init__(self,
                name,
                study = None,
                current_trial = None,
                algorithm = "BayesianOptimization",
                early_stop = None,
                early_stop = "MedianStop"
                create_time = None,
                update_time = None):

        self.name = name
        self.study = study
        self.current_trial = current_trial
        self.algorithm = algorithm
        self.create_time = create_time
        self.update_time = update_time
        self.search = search
        self.early_stop = early_stop
        self.trials_history_for_earlystop = []
        self.trials_history = []

    
    def _should_trial_stop(self,trial_metric,trial):
        if self.early_stop== None:
            raise Exception("Wrong Search Type")
        return self.early_stop(self.study,self.trials_history,trial_metric)

        

    def _add_measurement_to_trial(self,trial_metric,trial):
        trial.status = "Pending"
        trial.metric = trial_metric
        self.trials_history_for_earlystop.append(copy.deepcopy(trial))
    
    def _complete_trial(self,trial_metric,trial)
        trial.status = "Complete"
        trial.metric = trial_metric
        self.trials_history.append(copy.deepcopy(trial))
        
    
    def _get_next_trials(self):

        if self.search == None:
            raise Exception("Wrong Search Type")
        self.current_trial = self.search._get_next_trial(self.study,trials_list = self.study.configuration['trial_list'],number = self.study.configuration['number'])
        self.current_trial._info()
        return self.current_trial

    def _get_study_name(self):
        return self.study.name
    
    @classmethod
    def fromjson(self,json_file):

        study = Study._from_json(json_file)
        if study.algorithm == "GridSearch":
            self.search = GridSearch()
        elif study.algorithm == "RandomSeach":
            self.search = RandomSearch()     
        elif study.algorithm == "BayesianOptimization":
            self.search = BayesianOptimization()
        elif study.algorithm == "TpeAlgorithm":
            self.search = TpeAlgorithm()
        elif study.algorithm == "CmaesAlgorithm":
            self.search = CmaesAlgorithm()
        elif study.algorithm == "SimulateAnnealAlgorithm":
            self.search = SimulateAnnealAlgorithm()
        else:
            self.search = BayesianOptimization()
        
        if study.earlystop != None:
            if study.earlystop['name'] == "MedianStop":
                earlystop = MedianStop
            elif study.earlystop['name'] == "CurveFitting":
                earlystop = CurveFitting
            else:
                earlystop = None

        
        return Worker(self.study.name + '_Worker',study = study,current_trial=None,algorithm=study.algorithm,earlystop=earlystop,create_time=time.time(),update_time==time.time())



        

