'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-19 09:46:42
@LastEditors: feliciaren
@LastEditTime: 2020-05-19 11:06:32
'''

import numpy as np
import time
import logging
import random
import math

from server.model.study import Study 
from server.model.trials import Trials 
from server.search.basic_search import BasicSearch
from server.search.bayesian_optimization import BayesianOptimization

class HyperBandSearch(BasicSearch):

   def _get_next_trial(self,study=None,trials_list = [],number = 1):

        """
        Hyperband paper <http://www.jmlr.org/papers/volume18/16-558/16-558.pdf>
        """

        logging.info('HyperBandSearch, need number{}'.format(number))

        assert(study.__class__==Study)
        self.params = study.configuration
        self.study_name = study.name
        self.goal = study.goal
        self.study = study


        self.R=60
        self.eta=3
        self.s_max = math.floor(math.log(self.R, self.eta))
        self.B = (self.s_max + 1) * self.R
        self.n = math.ceil((self.s_max + 1) * (self.eta ** self.s_max) / (self.s_max + 1))
        self.r = self.R/(math.pow(self.eta,self.s_max))


        if len(trials_list) < self.n:
            bayes= BayesianOptimization()
            return_trials = bayes._get_next_trial(self.study, trials_list, number)
            return return_trials
        
        i = random.randint(0,3)
        ni = math.ceil(self.n / (math.pow(self.eta,i)))
        ri = self.r * i

        return_trials = bayes._get_next_trial(self.study, trials_list, ri)

        return return_trials