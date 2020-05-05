'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-02 18:48:48
@LastEditors: feliciaren
@LastEditTime: 2020-02-23 23:28:25
'''
__all__ = ['Trials']
import time

class Trials(object):

    
    def __init__(self,
                study_name,
                params = None,
                status = "ToDo",
                create_time = None,
                update_time = None,
                train_step = 10,
                metric = None,
                id = None
                ):
        self.study_name = study_name
        self.status = status
        self.params = params
        self.create_time = create_time
        self.update_time = update_time
        # self.train_step = train_step
        self.metric = metric
        self.id = id
    
    def __len__(self):
        return len(self.params)
    
    def _get_status(self):
        return self.status
    
    def _info(self):
        print("================{}_{}================".format(self.study_name,self.id))
        print("ID: {}, Create Time: {}, Update Time:{}".format(self.id,time.asctime(time.localtime(self.create_time)),time.asctime(time.localtime(self.update_time))))
        print("Parameters:")
        for key in self.params:
            print("{}: {}".format(key,self.params[key]))
        print("Metics:", self.metric)
    
    def _to_dict(self,dic):
        return {'study_name':self.study_name,'status':self.status,
                'params':self.params,'create_time':self.create_time,'update_time':self.update_time,
                'metric':self.metric,'id':self.id}

    @classmethod
    def _from_dict(self,dic):
        return Trials(study_name = dic['study_name'], params = dic['params'],
                        status = dic['status'], create_time = dic['create_time'],
                        update_time = dic['update_time'],
                        metric = dic['metric'],id = dic['id']
                        )