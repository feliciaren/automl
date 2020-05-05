'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-04-12 18:43:11
@LastEditors: feliciaren
@LastEditTime: 2020-04-12 18:49:47
'''
from .base_chocolate_algorithm import BaseChocolateAlgorithm


class CmaesAlgorithm(BaseChocolateAlgorithm):
  """
  Get the new suggested trials with CMAES algorithm.
  """

  def __init__(self,study):
    super(CmaesAlgorithm, self).__init__("CMAES", study)