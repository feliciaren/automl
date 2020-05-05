'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-04-12 17:13:03
@LastEditors: feliciaren
@LastEditTime: 2020-04-12 17:29:37
'''
from .base_hyperopt_algorithm import BaseHyperoptAlgorithm


class SimulateAnnealAlgorithm(BaseHyperoptAlgorithm):
  """
  Get the new suggested trials with simulate anneal algorithm.
  """

  def __init__(self,study = None):
    super(SimulateAnnealAlgorithm, self).__init__("anneal",study)
