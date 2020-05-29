'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-04-12 17:04:10
@LastEditors: feliciaren
@LastEditTime: 2020-05-20 09:08:40
'''


import itertools
import time
import json
import numpy as np
import hyperopt
import logging

from server.search.basic_search import BasicSearch
from server.model.study import Study 
from server.model.trials import Trials 



class BaseHyperoptAlgorithm(BasicSearch):
    def __init__(self, algorithm_name="tpe"):

        if algorithm_name == 'tpe':
            self.hyperopt_algorithm = hyperopt.tpe.suggest
        elif algorithm_name == 'random_search':
            self.hyperopt_algorithm = hyperopt.rand.suggest
        elif algorithm_name == 'anneal':
            self.hyperopt_algorithm = hyperopt.anneal.suggest
            
        self.algorithm_name = algorithm_name
        

    def _get_next_trial(self, study = None,trials_list=[], number=1):
        """
        Get the new suggested trials with TPE algorithm.
        """
        logging.info('{}Algorithm, need number{}'.format(self.algorithm_name,number))
        assert(study.__class__==Study)
        self.study = study
        # Construct search space, example: {"x": hyperopt.hp.uniform('x', -10, 10), "x2": hyperopt.hp.uniform('x2', -10, 10)}
        hyperopt_search_space = {}

        study = self.study
        params = study.configuration
        # params = study_configuration_json["params"]

        for param in params:
            param_name = param["parameterName"]

            if param["type"] == "INTEGER":
                # TODO: Support int type of search space)
                hyperopt_search_space[param_name] = hyperopt.hp.quniform(
                    param_name, param["minValue"], param["maxValue"],1)

            elif param["type"] == "DOUBLE":
                hyperopt_search_space[param_name] = hyperopt.hp.uniform(
                    param_name, param["minValue"], param["maxValue"])

            elif param["type"] == "DISCRETE":
                feasible_points = param["feasiblePoints"]
                hyperopt_search_space[param_name] = hyperopt.hp.choice(
                    param_name, feasible_points)
                # print(1,param_name,feasible_points)

            elif param["type"] == "CATEGORICAL":
                feasible_points = param["feasiblePoints"]
                hyperopt_search_space[param_name] = hyperopt.hp.choice(
                    param_name, feasible_points)
                

        # New hyperopt variables
        hyperopt_rstate = np.random.RandomState()
        hyperopt_domain = hyperopt.Domain(None, hyperopt_search_space, pass_expr_memo_ctrl=None)

        hyperopt_trial_specs = []
        hyperopt_trial_results = []
        # Example: # Example: [{'tid': 0, 'idxs': {'l1_normalization': [0], 'learning_rate': [0], 'hidden2': [0], 'optimizer': [0]}, 'cmd': ('domain_attachment', 'FMinIter_Domain'), 'vals': {'l1_normalization': [0.1], 'learning_rate': [0.1], 'hidden2': [1], 'optimizer': [1]}, 'workdir': None}]
        hyperopt_trial_miscs = []
        hyperopt_trial_new_ids = []

        # Update hyperopt for trained trials with completed advisor trials
        completed_hyperopt_trials = hyperopt.Trials()

        # completed_advisor_trials = Trial.objects.filter(
        #     study_name=study_name, status="Completed")
        completed_advisor_trials = [trial for trial in trials_list if trial.metric != None ]
        # print(len(completed_advisor_trials))

        for index, trial in enumerate(completed_advisor_trials):
        # Example: {"learning_rate": 0.01, "optimizer": "ftrl"}
            parameter_values_json = trial.params
            

            # Example: {'l1_normalization': [0], 'learning_rate': [0], 'hidden2': [0], 'optimizer': [0]}
            hyperopt_trial_miscs_idxs = {}
            # Example: {'l1_normalization': [0.1], 'learning_rate': [0.1], 'hidden2': [1], 'optimizer': [1]}
            hyperopt_trial_miscs_vals = {}
            new_id = index
            hyperopt_trial_new_ids.append(new_id)
            hyperopt_trial_misc = dict(
                tid=new_id, cmd=hyperopt_domain.cmd, workdir=hyperopt_domain.workdir)

            for param in params:

                if param["type"] == "INTEGER":
                    parameter_value = parameter_values_json[param["parameterName"]]
                    hyperopt_trial_miscs_idxs[param["parameterName"]] = [index]
                    hyperopt_trial_miscs_vals[param["parameterName"]] = [parameter_value]

                elif param["type"] == "DOUBLE":
                    parameter_value = parameter_values_json[param["parameterName"]]
                    hyperopt_trial_miscs_idxs[param["parameterName"]] = [index]
                    hyperopt_trial_miscs_vals[param["parameterName"]] = [parameter_value]

                elif param["type"] == "DISCRETE":
                #   feasible_points_string = param["feasiblePoints"]
                    feasible_points = param["feasiblePoints"]
                    parameter_value = parameter_values_json[param["parameterName"]]
                    index_of_value_in_list = feasible_points.index(parameter_value)
                    hyperopt_trial_miscs_idxs[param["parameterName"]] = [index]
                    hyperopt_trial_miscs_vals[param["parameterName"]] = [
                        index_of_value_in_list
                    ]
                    # print(2,index_of_value_in_list,parameter_value)

                elif param["type"] == "CATEGORICAL":
                    #   feasible_points_string = param["feasiblePoints"]
                    feasible_points = param["feasiblePoints"]
                    # Example: "ftrl"
                    parameter_value = parameter_values_json[param["parameterName"]]
                    index_of_value_in_list = feasible_points.index(parameter_value)
                    hyperopt_trial_miscs_idxs[param["parameterName"]] = [index]
                    hyperopt_trial_miscs_vals[param["parameterName"]] = [
                        index_of_value_in_list
                    ]
                   


            hyperopt_trial_specs.append(None)

            hyperopt_trial_misc["idxs"] = hyperopt_trial_miscs_idxs
            hyperopt_trial_misc["vals"] = hyperopt_trial_miscs_vals
            hyperopt_trial_miscs.append(hyperopt_trial_misc)

        # TODO: Use negative objective value for loss or not

            loss_for_hyperopt = trial.metric
            if study.goal == "MAXIMIZE":
                # Now hyperopt only supports fmin and we need to reverse objective value for maximization
                loss_for_hyperopt = -1 * trial.metric

            hyperopt_trial_result = {
                "loss": loss_for_hyperopt,
                "status": hyperopt.STATUS_OK
            }
            hyperopt_trial_results.append(hyperopt_trial_result)

            if len(completed_advisor_trials) > 0:
            # Example: {'refresh_time': datetime.datetime(2018, 9, 18, 12, 6, 41, 922000), 'book_time': datetime.datetime(2018, 9, 18, 12, 6, 41, 922000), 'misc': {'tid': 0, 'idxs': {'x2': [0], 'x': [0]}, 'cmd': ('domain_attachment', 'FMinIter_Domain'), 'vals': {'x2': [-8.137088361136204], 'x': [-4.849028446711832]}, 'workdir': None}, 'state': 2, 'tid': 0, 'exp_key': None, 'version': 0, 'result': {'status': 'ok', 'loss': 14.849028446711833}, 'owner': None, 'spec': None}
                hyperopt_trials = completed_hyperopt_trials.new_trial_docs(
                    hyperopt_trial_new_ids, hyperopt_trial_specs, hyperopt_trial_results,
                    hyperopt_trial_miscs)
                for current_hyperopt_trials in hyperopt_trials:
                    current_hyperopt_trials["state"] = hyperopt.JOB_STATE_DONE

            completed_hyperopt_trials.insert_trial_docs(hyperopt_trials)
            completed_hyperopt_trials.refresh()

        rval = hyperopt.FMinIter(
            self.hyperopt_algorithm,
            hyperopt_domain,
            completed_hyperopt_trials,
            max_evals=-1,
            rstate=hyperopt_rstate,
            verbose=0)
        rval.catch_eval_exceptions = False

        new_ids = rval.trials.new_trial_ids(number)

        rval.trials.refresh()

        random_state = rval.rstate.randint(2**31 - 1)
        new_trials = self.hyperopt_algorithm(
            new_ids, rval.domain, completed_hyperopt_trials, random_state)
        rval.trials.refresh()

        # Construct return advisor trials from new hyperopt trials
        return_list = []

        for i in range(number):

        # Example: {u'hidden2': [2], u'learning_rate': [0.04633366105812467], u'l1_normalization': [0.16858448611765364], u'optimizer': [3]}
            vals = new_trials[i]['misc']['vals']

            #   new_advisor_trial = Trial.create(study.name, "TpeTrial")
            parameter_values_json = {}

            for param in params:

                if param["type"] == "INTEGER":
                    suggest_value = int(vals[param["parameterName"]][0])
                    # print(type(suggest_value))
                    parameter_values_json[param["parameterName"]] = int(suggest_value)

                elif param["type"] == "DOUBLE":
                    suggest_value = vals[param["parameterName"]][0]
                    parameter_values_json[param["parameterName"]] = suggest_value

                elif param["type"] == "DISCRETE":
                    feasible_point_list = param["feasiblePoints"]
                    suggest_index = vals[param["parameterName"]][0]
                    suggest_value = feasible_point_list[suggest_index]
                    # print(3,suggest_index,suggest_value)

                elif param["type"] == "CATEGORICAL":
                    feasible_point_list = param["feasiblePoints"]
                    suggest_index = vals[param["parameterName"]][0]
                    suggest_value = feasible_point_list[suggest_index]
                    

                parameter_values_json[param["parameterName"]] = suggest_value

            new_trial = Trials(study_name = self.study.name,params=parameter_values_json,create_time=time.time(),update_time=time.time())
            # trials_list.append(new_trial)
            return_list.append(new_trial)

        return return_list 
