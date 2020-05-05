'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-04-12 18:23:11
@LastEditors: feliciaren
@LastEditTime: 2020-05-05 21:26:59
'''
import json
import chocolate as choco
import time


from server.search.basic_search import BasicSearch
from server.model.study import Study 
from server.model.trials import Trials 


class BaseChocolateAlgorithm(BasicSearch):
  def __init__(self, algorithm_name="QuasiRandom"):

    self.algorithm_name = algorithm_name


  def _get_next_trial(self, study,trial_list=[], number=1):
    """
    Get the new suggested trials with Chocolate algorithm.
    """
    assert(study.__class__==Study)
    self.study = study

    # 1. Construct search space
    # Example: {"x" : choco.uniform(-6, 6), "y" : choco.uniform(-6, 6)}
    chocolate_search_space = {}

    study = self.study
    params = study.configuration

    for param in params:
      param_name = param["parameterName"]

      if param["type"] == "INTEGER":
        # TODO: Support int type of search space)
        pass

      elif param["type"] == "DOUBLE":
        chocolate_search_space[param_name] = choco.uniform(
            param["minValue"], param["maxValue"])

      elif param["type"] == "DISCRETE" or param["type"] == "CATEGORICAL":
        feasible_points = param["feasiblePoints"]
        chocolate_search_space[param_name] = choco.choice(feasible_points)

    conn = choco.SQLiteConnection("sqlite:///my_db.db")

    # Refer to https://chocolate.readthedocs.io/tutorials/algo.html
    if self.algorithm_name == "Grid":
      sampler = choco.Grid(conn, chocolate_search_space, clear_db=True)
    elif self.algorithm_name == "Random":
      sampler = choco.Random(conn, chocolate_search_space, clear_db=True)
    elif self.algorithm_name == "QuasiRandom":
      sampler = choco.QuasiRandom(conn, chocolate_search_space, clear_db=True)
    elif self.algorithm_name == "Bayes":
      sampler = choco.Bayes(conn, chocolate_search_space, clear_db=True)
    elif self.algorithm_name == "CMAES":
      sampler = choco.CMAES(conn, chocolate_search_space, clear_db=True)
    elif self.algorithm_name == "MOCMAES":
      mu = 1
      sampler = choco.MOCMAES(
          conn, chocolate_search_space, mu=mu, clear_db=True)

    # 2. Update with completed advisor trials
    # completed_advisor_trials = Trial.objects.filter(
    #     study_name=study_name, status="Completed")
    completed_advisor_trials = trial_list[:-1]

    for index, trial in enumerate(completed_advisor_trials):
      parameter_values_json = trial.params

      loss = trial.metric
      if study.goal == "MAXIMIZE":
        loss = -1 * loss

      entry = {"_chocolate_id": index, "_loss": loss}
      entry.update(parameter_values_json)
      # Should not use sampler.update(token, loss)
      conn.insert_result(entry)

    # 3. Run algorithm and construct return advisor trials
    return_list = []

    for i in range(number):

      # Example: {'_chocolate_id': 1}
      # Example: {u'hidden2': u'32', u'learning_rate': 0.07122424534644338, u'l1_normalization': 0.8402644688674471, u'optimizer': u'adam'}
      token, chocolate_params = sampler.next()

      parameter_values_json = {}

      for param in params:

        if param["type"] == "INTEGER" or param["type"] == "DOUBLE" or param["type"] == "CATEGORICAL":
          parameter_values_json[param["parameterName"]] = chocolate_params[
              param["parameterName"]]
        elif param["type"] == "DISCRETE":
          parameter_values_json[param["parameterName"]] = int(
              chocolate_params[param["parameterName"]])

      new_trial = Trials(study_name = self.study.name,params=parameter_values_json,create_time=time.time(),update_time=time.time())
      trial_list.append(new_trial)
      return_list.append(new_trial)

    return return_list
