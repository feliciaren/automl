import json
import os


class Worker(object):

    def __init__(self,
                name,
                study = None,
                current_trial = None,
                algorithm = "BayesianOptimization",
                create_time = None,
                update_time = None):

        self.name = name
        self.study = study
        self.current_trial = current_trial
        self.algorithm = algorithm
        self.create_time = create_time
        self.update_time = update_time
    
    def _early_stop():
        
    
    def _get_next_step()