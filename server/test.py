'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-06 17:33:55
@LastEditors: feliciaren
@LastEditTime: 2020-05-06 22:13:44
'''
from model.cmd import entry_point
from model.worker import Worker

request = {
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
            }]
        }

model = Worker._from_json(request)
res = model.test_get_next_trials()
print(res)