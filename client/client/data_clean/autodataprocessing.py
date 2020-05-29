'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-12 18:38:46
@LastEditors: feliciaren
@LastEditTime: 2020-05-17 22:36:28
'''

import json
import os
import sys
import numpy as np
import logging

from client.data_clean.config import *
from client.data_clean.label_process import LabelProcess
from client.data_clean.feature_process import FeatureProcess
from client.data_clean.stringindex import StringIndex

class AutoDataProcess(object):
    def __init__(self, max_label_value_num = sys.maxsize, missing_threshold=0.99,
                task_type=BINARY_CLASSIFICATION, label_col=None):
        
        self.label_col = label_col
        self.max_label_value_num = max_label_value_num
        self.missing_threshold = missing_threshold
        self.task_type = task_type
        self.feature_process = FeatureProcess(self.missing_threshold)
        self.label_process = None
        self.label_string2index = None

        logging.debug("AutoDataProcessing init")
        
    def _fit_(self,dataset):

        logging.debug("AutoDataProcessing _fit_ start")

        dataset = np.array(dataset)
        return_label = None
        if self.label_col != None:
            label = dataset[:,self.label_col]
            self.label_process = LabelProcess(label,self.task_type,self.max_label_value_num)
            label = self.label_process.process(label)
            if self.task_type in CLASSIFICATION_TASKS:
                self.label_string2index = StringIndex(inputcol = label)
                return_label = self.label_string2index._fit_(label)
            else:
                return_label = label
            logging.debug("AutoDataProcessing _fit_ label data finish")
            feature = np.delete(dataset,self.label_col,axis=1)
        else:
            feature = dataset
        return_feature = self.feature_process._fit_(feature)
        logging.debug("AutoDataProcessing _fit_ feature data finish")
        logging.debug("AutoDataProcessing _fit_ finish")
        return return_feature,return_label
    

    def _transform_(self,dataset,label_col = None):
        logging.debug("AutoDataProcessing _transform_ start")
        dataset = np.array(dataset)
        return_label = None
        if self.label_col != None:
            label = dataset[:,self.label_col]
            self.label_process = LabelProcess(label,self.task_type,self.max_label_value_num)
            label = self.label_process.process(label,transform=True)
            if self.task_type in CLASSIFICATION_TASKS:
                return_label = self.label_string2index._transform_(label)
            else:
                return_label = label
            logging.debug("AutoDataProcessing _transform_ label data finish")
            feature = np.delete(dataset,self.label_col,axis=1)
        else:
            feature = dataset
        return_feature = self.feature_process._transform_(feature)
        logging.debug("AutoDataProcessing _transform_ feature data finish")
        logging.debug("AutoDataProcessing _transform_ finish")
        return return_feature,return_label
    



            
        

        



