'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-05 21:04:33
@LastEditors: feliciaren
@LastEditTime: 2020-05-20 09:10:28
'''
import random
from server.model.study import Study
from server.search.tpe import TpeAlgorithm

class TestTpeAlgorithm:
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
        tpe = TpeAlgorithm()
        assert(tpe.__class__==TpeAlgorithm)

    def test_get_next_trial(self):
        tpe = TpeAlgorithm()
        trials_list = []
        for i in range(5):
            next_trial = tpe._get_next_trial(self.study,trials_list,1)

            assert(len(next_trial)== 1)

            new_trial = next_trial[0]
            new_trial_json = new_trial.params

            assert(new_trial_json["hidden"] in [8,16,32])
            assert(new_trial_json["optimizer"] in ["sgd", "adagrad"])
            assert(new_trial_json["batch_normalization"] in [True,False])
            assert(new_trial_json["learning_rate"] >= 0.01)

            next_trial[0].metric = random.random()
            trials_list.extend(next_trial)

if __name__ == "__main__":
    test = TestTpeAlgorithm()
    test.setup()
    test.test_init()
    test.test_get_next_trial()