'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-05 22:13:27
@LastEditors: feliciaren
@LastEditTime: 2020-05-05 22:13:27
'''
import abc


class AbstractEarlyStopAlgorithm(object):

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def _get_early_stop_trials_(self, trials):
    """
    判断算法当前试验是否需要提前终止
    
    Args:
      trials: 当前参数配置已完成的所有试验.
    Returns:
      实验是否需要提前终止.
    """
    pass