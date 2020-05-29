'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-23 14:53:01
@LastEditors: feliciaren
@LastEditTime: 2020-05-20 09:03:38
'''
__all__ = ['BayesianOptimization']
import numpy as np
import time
import logging

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern

from server.search.basic_search import BasicSearch
from server.search.random_search import RandomSearch
from server.model.study import Study 
from server.model.trials import Trials 

class BayesianOptimization(BasicSearch):

    def _get_next_trial(self,study=None,trials_list = [],number = 1):

        logging.info('BayesianOptimization, need number{}'.format(number))

        assert(study.__class__==Study)
        self.params = study.configuration
        self.study_name = study.name
        self.goal = study.goal
        self.study = study

        self.bounds = []

        for param in self.params:
            if param["type"] == "DOUBLE" or param["type"] == "INTEGER":
                min_value = param["minValue"]
                max_value = param["maxValue"]
                self.bounds.append((min_value, max_value))

            elif param["type"] == "DISCRETE":
                feasible_points = param["feasiblePoints"]
                for feasible_point in feasible_points:
                    self.bounds.append((0, 1))

            elif param["type"] == "CATEGORICAL":
                feasible_points = param["feasiblePoints"]
                for feasible_point in feasible_points:
                    self.bounds.append((0, 1))

            # Make sure it is numpy ndarry
        self.bounds = np.asarray(self.bounds)

        random_init_trial_number = 3
        number = 1
        completed_trials_list = [trial for trial in trials_list if trial.metric != None ]
        # print(len(completed_trials_list))
        # Use random search if it has less dataset
        if len(completed_trials_list) < random_init_trial_number:
            randomSearch= RandomSearch()
            return_trials = randomSearch._get_next_trial(self.study, completed_trials_list, number)
            return return_trials
        

        # Construct data to train gaussian process, Example: [[50], [150], [250]]
        init_points = []
        # Example: [0.6, 0.8, 0.6]
        init_labels = []

        # Construct train data with completed trials
        for trial in completed_trials_list:
        # Example: {"learning_rate": 0.01, "optimizer": "ftrl"}
            # Example: [0.01, "ftrl"]
            param_dic = trial.params
            instance_features = []
            instance_label = trial.metric

            for param in self.params:

                if param["type"] == "DOUBLE" or param["type"] == "INTEGER":
                    instance_feature = param_dic[param["parameterName"]]
                    instance_features.append(instance_feature)

                elif param["type"] == "DISCRETE":
                    feasible_points = param["feasiblePoints"]
                    parameter_value = param_dic[param["parameterName"]]
                    for feasible_point in feasible_points:
                        if feasible_point == parameter_value:
                            instance_features.append(1)
                        else:
                            instance_features.append(0)
                elif param["type"] == "CATEGORICAL":
                    # Example: ["sgd", "adagrad", "adam", "ftrl"]
                    feasible_points = param["feasiblePoints"]
                    # Example: "ftrl"
                    parameter_value = param_dic[param["parameterName"]]
                    for feasible_point in feasible_points:
                        if feasible_point == parameter_value:
                            instance_features.append(1)
                        else:
                            instance_features.append(0)

        init_points.append(instance_features)
        init_labels.append(instance_label)

        # Example: ndarray([[ 50], [150], [250]])
        train_features = np.asarray(init_points)
        # Example: ndarray([0.6, 0.8, 0.6])
        train_labels = np.asarray(init_labels)
        # current_max_label = train_labels.max()

        # Train with gaussian process
        gp = GaussianProcessRegressor(
            kernel=Matern(nu=2.5),
            n_restarts_optimizer=25, )

        gp.fit(train_features, train_labels)

        # Example: [[-3.66909025, -0.84486644], [-1.93270006, -0.95367483], [1.36095631, 0.61358525], ...], shape is [100000, 2]
        x_tries = np.random.uniform(
            self.bounds[:, 0], self.bounds[:, 1], size=(100000, self.bounds.shape[0]))

        mean, std = gp.predict(x_tries, return_std=True)

        # Construct the map of name and scope to compute gaussian process
        acquisition_function_kappa = 5

        # Confidence bound criteria
        acquisition_fucntion_values = mean + acquisition_function_kappa * std


        if self.goal == "MAXIMIZE":
            x_max = x_tries[acquisition_fucntion_values.argmax()]
        #max_acquision_fucntion_value = acquisition_fucntion_values.max()
        elif self.goal == "MINIMIZE":
            x_max = x_tries[acquisition_fucntion_values.argmin()]
        #max_acquision_fucntion_value = acquisition_fucntion_values.min()
        else:
        # TODO: Throw the error
            x_max = []

        # Example: [3993.864683994805, 44.15441513231316]
        x_max = np.clip(x_max, self.bounds[:, 0], self.bounds[:, 1])
        # print("Current max acquision function choose: {}".format(x_max))

        # Example: {"hidden2": 3993.864683994805, "hidden1": 44.15441513231316}
        suggested_dict = {}

        index = 0

        for param in self.params:

            if param["type"] == "DOUBLE":
                suggested_dict[param["parameterName"]] = x_max[index]
                index += 1

            elif param["type"] == "INTEGER":
                suggested_dict[param["parameterName"]] = int(x_max[index])
                index += 1

            elif param["type"] == "DISCRETE":
                feasible_points = param["feasiblePoints"]
                # Find the max value of these and get its string
                current_max = x_max[index]
                suggested_parameter_value = feasible_points[0]

                for feasible_point in feasible_points:
                    if x_max[index] > current_max:
                        current_max = x_max[index]
                        suggested_parameter_value = feasible_point
                    index += 1

                suggested_dict[param["parameterName"]] = suggested_parameter_value

            elif param["type"] == "CATEGORICAL":
                feasible_points = param["feasiblePoints"]
                # Example: ["sgd", "adagrad", "adam", "ftrl"]

                # Find the max value of these and get its string
                current_max = x_max[index]
                suggested_parameter_value = feasible_points[0]

                for feasible_point in feasible_points:
                    if x_max[index] > current_max:
                        current_max = x_max[index]
                        suggested_parameter_value = feasible_point
                    index += 1

                suggested_dict[param["parameterName"]] = suggested_parameter_value

        new_trial = Trials(study_name = self.study_name,params=suggested_dict,create_time=time.time(),update_time=time.time())
        # trials_list.append(new_trial)
        return [new_trial]
    
        
