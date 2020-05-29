'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-12 14:58:49
@LastEditors: feliciaren
@LastEditTime: 2020-05-17 22:34:55
'''
import sys
import logging

from client.data_clean.utils import Utils
from client.data_clean.config import *
from client.data_clean.stringindex import StringIndex



class LabelProcess(object):

    def __init__(self,label,task_type,max_label_count = sys.maxsize):
        
        self.ori_label = label
        self.num_label = list(set(self.ori_label))
        self.num_class = len(self.num_label)
        self.task_type = task_type
        logging.debug('LabelProcess init')
    
    def process(self,dataset,transform = False):
        logging.info('LabelProcess process start')

        if transform == False:

            if self.task_type == BINARY_CLASSIFICATION and self.num_class > 2:
                raise Exception("binary classification task only handle 2 class,"
                                " but the label class has {}".format(self.num_class))

            if self.task_type == MULTICLASS_CLASSIFICATION and self.num_class > self.max_label_count:
                raise Exception("The label number is too big and the max label number is {}".format(self.max_label_count))

            if self.num_class <= 1:
                raise Exception("The label number is only : {} and can't to classify or regression".format(self.num_class))
        
        result_type = [Utils().check_type(i) for i in self.ori_label]
        result_type = [i for i in result_type if i != NAN]

        # task_type is regression, string to double
        if self.task_type == REGRESSION:
            
            if STRING in result_type:
                raise Exception("The label value is string")
            
            result_df = [Utils().numerical_string_to_double(i) for i in self.ori_label]
            logging.info('task type REGRESSION and lable type string, StringToDouble')
        # task type CLASSIFICATION_TASKS and lable type to string
        elif self.task_type in CLASSIFICATION_TASKS:

            flag = 0
            for i in result_type:
                if i != STRING:
                    flag = 1
                    break
            
            if flag != 0:
                result_df = [Utils().to_str(i) for i in self.ori_label]
            logging.info('task type CLASSIFICATION_TASKS and lable type string')
            
        else:
            raise Exception("Unsupported the task_type %s" % self.task_type)

        logging.info('LabelProcess process finish')

        return result_df
    
    


