'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-03-23 12:01:33
@LastEditors: feliciaren
@LastEditTime: 2020-05-06 10:03:53
'''
import abc
__all__ = ['BasicSelector']
class BasicSelector(object):
    __metaclass__ = abc.ABCMeta

    
    @abc.abstractmethod
    def _fit_(self,x,y):
        """
        将数据拟合到 FeatureSelector

        Args:
        ------------
        X : numpy 矩阵.训练输入样本，shape: [n_samples, n_features]。
        y: numpy 矩阵目标值 (分类中的类标签，回归中为实数)。 shape是 [n_samples]。
        """
        self.X = X
        self.y = y

    @abc.abstractmethod
    def _get_selected_feature(self):
        """
        获取重要特征

        Returns
        -------
        list :
        返回重要特征的索引。
        """
        pass