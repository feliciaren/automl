'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-25 09:01:17
@LastEditors: feliciaren
@LastEditTime: 2020-05-29 18:42:20
'''
import random
from client.model.worker import Worker


class TestEarlyStop:
    def setup(self):
        self.study_configuration_json = {
            "goal":
            "MAXIMIZE",
            "maxTrials":
            5,
            "maxParallelTrials":
            1,
            "randomInitTrials":
            1,
            "earlystop":{
                "target_pos" : 10,
                "trials_history" : [],
                "trial_metric" : 1,
            },
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
                "feasiblePoints": ['true','false'],
                "scalingType": "LINEAR"
            },{
                "parameterName": "learning_rate",
                "type": "DOUBLE",
                "minValue": 0.01,
                "maxValue": 0.5,
                "scalingType": "LINEAR"
            }]
        }
        self.url = 'http://127.0.0.1:8686'


    def test_get_next_trial(self):
        worker = Worker()._from_json(self.study_configuration_json)
        trial_list = []
        for i in range(5):
            res = worker._get_next_trials(self.url,trial_list,1)
            # print(res)
            trial_list.append(res._to_dict())
            trial_list[-1]['metric'] = random.random()

    

if __name__ == "__main__":
    
    test = TestEarlyStop()
    test.setup()
    test.test_get_next_trial()


