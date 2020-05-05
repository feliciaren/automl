'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-04-12 17:11:51
@LastEditors: feliciaren
@LastEditTime: 2020-04-12 17:29:28
'''
from .base_hyperopt_algorithm import BaseHyperoptAlgorithm


class TpeAlgorithm(BaseHyperoptAlgorithm):
  """
  Get the new suggested trials with TPE algorithm.
  """

  def __init__(self,study = None):
    super(TpeAlgorithm, self).__init__("tpe",study)
