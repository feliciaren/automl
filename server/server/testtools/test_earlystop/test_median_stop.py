'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-05 19:09:42
@LastEditors: feliciaren
@LastEditTime: 2020-05-20 09:08:27
'''

import random

from server.model.study import Study
from server.search.random_search import RandomSearch
from server.early_stop.median_stop import MedianStop


class TestMedianStop:
    
    def setup(self):
        study_configuration_json = {
            "goal":
            "MAXIMIZE",
            "maxTrials":
            5,
            "maxParallelTrials":
            1,
            "randomInitTrials":
            1,
            "params": [{
                "parameterName": "hidden",
                "type": "DISCRETE",
                "feasiblePoints": [8,16,32],
                "scalingType": "LINEAR"
            }, {
                "parameterName": "optimizer",
                "type": "CATEGORICAL",
                "feasiblePoints": ["sgd", "adagrad"],
                "scalingType": "LINEAR"
            }, {
                "parameterName": "batch_normalization",
                "type": "CATEGORICAL",
                "feasiblePoints": [True,False],
                "scalingType": "LINEAR"
            },{
                "parameterName": "learning_rate",
                "type": "DOUBLE",
                "minValue": 0.01,
                "maxValue": 0.5,
                "scalingType": "LINEAR"
            }]
        }
        self.study = Study._from_dict(study_configuration_json)



    def test_init(self):
        stop = MedianStop()
        assert(stop.__class__==MedianStop)

    
    def test_should_early_stop(self):

        randomsearch = RandomSearch()
        stop = MedianStop()
        self.trials_list =  []
        for i in range(5):
            next_trial = randomsearch._get_next_trial(self.study,self.trials_list,1)
            next_trial[0].metric = random.random()
            self.trials_list.extend(next_trial)
            result = stop._should_early_stop(self.study,self.trials_list,random.random())
            assert(result in [True, False])

