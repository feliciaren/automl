'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-12 20:19:54
@LastEditors: feliciaren
@LastEditTime: 2020-05-17 21:25:20
'''

import numpy as np
import logging

from client.data_clean.utils import Utils
from client.data_clean.config import *

class Statistic(object):

    @staticmethod
    def statistic(dataset):

        logging.info('Statistic start')

        missing_cols = []
        missing_nums = []
        datatype = []
        dataset = np.array(dataset)
        for i in range(len(dataset[0])):
            col = dataset[:,i]
            col_type = [Utils().check_type(d) for d in col]
            count_pre = len(col_type)
            if NAN in col_type:
                col_type = [r for r in col_type if r != NAN]
            count_after = len(col_type)
            missing_nums.append(count_after-count_pre)
            
            if col_type == []:
                missing_cols.append(i)
                datatype.append(NAN)
            
            else:
                col_type = list(set(col_type))
                if len(col_type) == 1:
                    datatype.append(col_type[0])
                else:
                    datatype.append(STRING)

        logging.info('Statistic finish, missing_cols: {},missing_nums: {},datatype: {}'.format(missing_cols,missing_nums,datatype))
        
        return missing_cols,missing_nums,datatype
            

            
