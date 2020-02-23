'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-02 18:48:48
@LastEditors: feliciaren
@LastEditTime: 2020-02-22 19:50:49
'''
class Trials(object):

    
    def __init__(self,
                study_name,
                paras = None,
                status = None,
                create_time = None,
                update_time = None,
                train_step = 10,
                metric = None,
                id = None
                ):
        self.study_name = study_name
        self.status = status
        self.paras = paras
        self.create_time = create_time
        self.update_time = update_time
        self.train_step = train_step
        self.metric = metric
        self.id = id
    
    def __len__(self):
        return len(self.paras)
    
    def _get_status(self):
        return self.status
    
    def _info(self):
        print("================{}_{}================".format(self.study_name,self.id))
        print("ID: {}, Create Time: {}, Update Time:{}, Train Step:{}".format(self.id,self.create_time,self.update_time,self.train_step))
        print("Parameters:")
        for key in self.paras:
            print("{}: {}".format(key,self.paras[key]))
        print("Metics:")
        for key in self.metric:
            print("{}: {}".format(key,self.metric[key]))
    
    def _to_dict(self,dic):
        return {'study_name':self.study_name,'status':self.status,
                'paras':self.paras,'create_time':self.create_time,'update_time':self.update_time,
                'train_step':self.train_step,'metric':self.metric,'id':self.id}

    @classmethod
    def _from_dict(self,dic):
        return Trials(study_name = dic['study_name'], paras = dic['paras'],
                        status = dic['status'], create_time = dic['create_time'],
                        update_time = dic['update_time'], train_step = dic['train_step'],
                        metric = dic['metric'],id = dic['id']
                        )