'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-05 22:13:27
@LastEditors: feliciaren
@LastEditTime: 2020-05-05 23:42:03
'''
import abc


class AbstractEarlyStopAlgorithm(object):

  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def _should_early_stop(self, study, trials_history,trial_metric):
    """
    判断算法当前试验是否需要提前终止
    
    Args:
      trials: 当前参数配置已完成的所有试验.
    Returns:
      实验是否需要提前终止.
    """
    pass