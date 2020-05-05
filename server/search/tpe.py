'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-04-12 17:11:51
@LastEditors: feliciaren
@LastEditTime: 2020-05-05 21:06:02
'''
from server.search.base_hyperopt_algorithm import BaseHyperoptAlgorithm


class TpeAlgorithm(BaseHyperoptAlgorithm):
  """
  Get the new suggested trials with TPE algorithm.
  """

  def __init__(self):
    super(TpeAlgorithm, self).__init__("tpe")
