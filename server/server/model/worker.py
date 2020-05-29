'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-02 18:48:48
@LastEditors: feliciaren
@LastEditTime: 2020-05-29 14:22:14
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
from server.search.evolution_search import EvolutionSearch
from server.search.hyperband_search import HyperBandSearch
from server.search.simulate_anneal import SimulateAnnealAlgorithm
from server.search.tpe import TpeAlgorithm
from server.early_stop.curve_stop import CurveStop
from server.early_stop.median_stop import MedianStop

__all__=['Worker']

class Worker(object):

    def __init__(self,
                name="worker",
                study = None,
                current_trial = None,
                algorithm = "BayesianOptimization",
                early_stop = "MedianStop",
                search = None,
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

    
    async def _should_trial_stop(self):
        if self.early_stop== None:
            raise Exception("Wrong Search Type")
        return self.early_stop(self.study,self.study.earlystop['trials_history'],self.study.earlystop['trial_metric'])

    async def startup(self,app):
        pass        

    def _add_measurement_to_trial(self,trial_metric,trial):
        trial.status = "Pending"
        trial.metric = trial_metric
        self.study.earlystop['trials_history'].append(copy.deepcopy(trial))
    
    def _complete_trial(self,trial_metric,trial):
        trial.status = "Complete"
        trial.metric = trial_metric
        self.study.trials_list.append(copy.deepcopy(trial))
        
    
    async def _get_next_trials(self):

        if self.search == None:
            raise Exception("Wrong Search Type")
        if self.study.trials_list != None:
            trials_list = self.study.trials_list
        else:
            trials_list = []
        
        if "number" in self.study.configuration:
            number = self.study.configuration['number']
        else:
            number = 1
            
        self.current_trial = self.search._get_next_trial(self.study,trials_list = trials_list,number = 1)
        for trial in self.current_trial:
            trial._info()
        return_list = [trial._to_dict() for trial in self.current_trial]
        return return_list
    
    def test_get_next_trials(self):

        if self.search == None:
            raise Exception("Wrong Search Type")
        if self.study.trials_list != None:
            trials_list = self.study.trials_list
        else:
            trials_list = []
        
        if "number" in self.study.configuration:
            number = self.study.configuration['number']
        else:
            number = 1
            
        self.current_trial = self.search._get_next_trial(self.study,trials_list = trials_list,number = 1)
        for trial in self.current_trial:
            trial._info()
        return_list = [trial._to_dict() for trial in self.current_trial]
        return return_list

    def _get_study_name(self):
        return self.study.name
    
    def _load_json(self,json):
        self.study = Study._from_dict(json)
        if self.study.algorithm == "GridSearch":
            self.search = GridSearch()
        elif self.study.algorithm == "RandomSeach":
            self.search = RandomSearch()     
        elif self.study.algorithm == "BayesianOptimization":
            self.search = BayesianOptimization()
        elif self.study.algorithm == "TpeAlgorithm":
            self.search = TpeAlgorithm()
        elif self.study.algorithm == "EvolutionSearch":
            self.search = EvolutionSearch()
        elif self.study.algorithm == "SimulateAnnealAlgorithm":
            self.search = SimulateAnnealAlgorithm()
        elif self.study.algorithm == "HyperBandSearch":
            self.search = HyperBandSearch()
        else:
            self.search = BayesianOptimization()
        
        if self.study.earlystop != None:
            if self.study.earlystop['name'] == "MedianStop":
                self.earlystop = MedianStop()
            elif self.study.earlystop['name'] == "CurveFitting":
                self.earlystop = CurveStop()
        else:
                self.earlystop = None
        
        self.name = str(self.study.name) + '_Worker'
        self.algorithm = self.study.algorithm
        self.create_time = time.time()
        self.update_time = time.time()
    
    @classmethod
    def _from_json(self,json_file):

        with open(json_file,'r',encoding='utf-8') as f:
            dic = json.load(f)

        self.study = Study._from_dict(dic)
        if self.study.algorithm == "GridSearch":
            self.search = GridSearch()
        elif self.study.algorithm == "RandomSeach":
            self.search = RandomSearch()     
        elif self.study.algorithm == "BayesianOptimization":
            self.search = BayesianOptimization()
        elif self.study.algorithm == "TpeAlgorithm":
            self.search = TpeAlgorithm()
        elif self.study.algorithm == "EvolutionSearch":
            self.search = EvolutionSearch()
        elif self.study.algorithm == "SimulateAnnealAlgorithm":
            self.search = SimulateAnnealAlgorithm()
        elif self.study.algorithm == "HyperBandSearch":
            self.search = HyperBandSearch()
        else:
            self.search = BayesianOptimization()
        
        if self.study.earlystop != None:
            if self.study.earlystop['name'] == "MedianStop":
                self.earlystop = MedianStop()
            elif self.study.earlystop['name'] == "CurveFitting":
                self.earlystop = CurveStop()
        else:
            self.earlystop = None

        
        return Worker(str(self.study.name) + '_Worker',study = self.study,current_trial=None,algorithm=self.study.algorithm,early_stop=self.study.earlystop,search = self.search,create_time=time.time(),update_time=time.time())

