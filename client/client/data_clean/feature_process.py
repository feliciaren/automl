'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-12 18:10:37
@LastEditors: feliciaren
@LastEditTime: 2020-05-17 22:37:47
'''

import logging 
import numpy as np

from client.data_clean.statistic import Statistic
from client.data_clean.utils import Utils
from client.data_clean.config import *
from client.data_clean.stringindex import StringIndex


class FeatureProcess(object):

    def __init__(self,missing_threshold=0.99):

        self.missing_threshold = missing_threshold
        self.missing_col = None
        self.delete_col = None
        self.datatype = None
        self.string2index = None

        logging.debug('Feature Processing init')
        
    
    def _fit_(self,dataset):

        logging.info('Feature Processing _fit_ start')

        self.missing_col,missing_nums ,datatype = Statistic().statistic(dataset)

        logging.info("Feature Processing _fit_ dataset Stastic missing col{},missing num{},datatype{}".format(self.missing_col,missing_nums,datatype))
        
        self.missing_col.reverse()

        dataset = np.array(dataset)

        if self.missing_col:
            for i in self.missing_col:
                np.delete(dataset,i,axis=1)
                datatype.pop(i)
        
        self.delete_col = []
        for i in missing_nums:
            if missing_nums[i] / len(dataset[i]) > self.missing_threshold:
                self.delete_col.append(i)
        self.delete_col.reverse()

        if self.delete_col:
            for i in self.delete_col:
                np.delete(dataset,i,axis=1)
                datatype.pop(i)

        self.datatype = datatype
        self.string2index = []
        result = []

        assert(len(dataset[0]) == len(self.datatype))

        for i in range(len(dataset[0])):

            if self.datatype[i] == STRING:
                stringindex = StringIndex(dataset[:,i])
                self.string2index.append(stringindex)
                result.append(stringindex._fit_(dataset[:,i]))
            
            else:

                result.append([Utils().numerical_string_to_double(d) for d in dataset[:,i].tolist()])
                self.string2index.append(None)
        
        logging.info('Feature Processing _fit_ finish')
        result = np.array(result)
        result = result.T
        result = result.tolist()
        return result
    
    def _transform_(self,dataset):

        logging.info('Feature Processing _transform_ start')

        dataset = np.array(dataset)

        if self.missing_col != None:
            for i in self.missing_col:
                np.delete(dataset,i,axis=1)
                
        if self.delete_col != None:
            for i in self.delete_col:
                np.delete(dataset,i,axis=1)

        assert(len(dataset[0]) == len(self.datatype))

        result = []

        for i in range(len(dataset[0])):

            if self.datatype[i] == STRING:
                result.append(self.string2index[i]._transform_(dataset[:,i]))
            
            else:
                result.append([Utils().numerical_string_to_double(d) for d in dataset[:,i].tolist()])
        
        logging.info('Feature Processing _transform_ finish')

        result = np.array(result)
        result = result.T
        result = result.tolist()
                
        return result


 




    
    

        