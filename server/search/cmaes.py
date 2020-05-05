'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-04-12 18:43:11
@LastEditors: feliciaren
@LastEditTime: 2020-05-05 21:26:45
'''
from server.search.base_chocolate_algorithm import BaseChocolateAlgorithm


class CmaesAlgorithm(BaseChocolateAlgorithm):
  """
  Get the new suggested trials with CMAES algorithm.
  """

  def __init__(self):
    super(CmaesAlgorithm, self).__init__("CMAES")