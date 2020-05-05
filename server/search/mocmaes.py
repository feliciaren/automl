'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-05 21:33:02
@LastEditors: feliciaren
@LastEditTime: 2020-05-05 21:33:58
'''
from server.search.base_chocolate_algorithm import BaseChocolateAlgorithm


class MocmaesAlgorithm(BaseChocolateAlgorithm):
  """
  Get the new suggested trials with MOCMAES algorithm.
  """

  def __init__(self):
    super(MocmaesAlgorithm, self).__init__("MOCMAES")
