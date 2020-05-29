'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-12 18:24:36
@LastEditors: feliciaren
@LastEditTime: 2020-05-17 22:18:37
'''
import logging
from client.data_clean.utils import *


class StringIndex(object):
    def __init__(self,inputcol = [],label2index = None, add_label = False):
        self.inputcol = inputcol
        self.label2index = label2index
        self.index2label = None
        self.add_label = add_label

        logging.debug('StringIndex init')


    def _fit_(self,dataset):

        logging.info('StringIndex _fit_ start')
        self.index2label = {}
        if self.label2index == None:
            self.label2index = {}
            if self.inputcol != []:
                self.label_num = list(set(self.inputcol))
                self.label_num = [Utils().to_str(i) for i in self.label_num]
                for i in range(len(self.label_num)):
                    self.label2index[self.label_num[i]] = i
                    self.index2label[str(i)] = self.label_num[i]
            else:
                raise  Exception("Please Input data or label2index dict")
        else:
            for key,value in self.label2index:
                self.index2label[str(value)] = key
        result_df = []
        for i in dataset:
            i = Utils().to_str(i)
            if i in self.label2index:
                result_df.append(int(self.label2index[i]))
            else:
                if self.add_label:
                    self.label_num.append(i)
                    self.label2index[i] = len(self.label_num)
                    self.index2label[str(len(self.label_num))] = i

                    result_df.append(int(self.label2index[i]))
                else:
                    raise  Exception("Wrong datatype {}, did not show in inputcol or label2index".format(i))
        
        logging.info('StringIndex _fit_ finish')
        return result_df
    
    def _transform_(self,dataset):

        logging.info('StringIndex _transform_ start')
        
        if self.label2index == None:
            raise  Exception("Please Input data or label2index dict and fit fuction first")

        result_df = []
        for i in dataset:
            i = Utils().to_str(i)
            if i in self.label2index:
                result_df.append(int(self.label2index[i]))
            else:
                raise  Exception("Wrong datatype {}, did not show in inputcol or label2index".format(i))
        
        logging.info('StringIndex _transform_ finish')
        return result_df   
