'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-06 09:27:15
@LastEditors: feliciaren
@LastEditTime: 2020-05-18 00:30:55
'''
import time
import copy
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from server.feature_select.gbdtselector import GBDTSelector
from server.feature_select.gradient_selector import FeatureGradientSelector

dataset_name = 'a1a'
feature_num = 123
num_class = 2
need_feature = 20

def preprocessing(lines):
    label = []
    data = []
    new_l = [0 for i in range(feature_num)]
    for line in lines:
        line = line.strip().split()
        label.append(eval(line.pop(0)))
        # new_line = [eval(i.split(':')[1]) for i in line]
        new_line = copy.deepcopy(new_l)
        for i in line:
            ids,num = i.split(':')
            new_line[eval(ids)-1] = num
        data.append(new_line)
    print("X shape: ",len(data[0]),len(data))
    print(data[0])
    
    labels = list(set(label))
    print("Y shape: ",len(labels),len(label))
    print(label[0])
    label_dic = {}
    for i in range(len(labels)):
        label_dic[labels[i]] = i
    
    new_label = []
    # new_l = [0 for i in range(len(labels))]
    for l in label:
    #     new = copy.deepcopy(new_l)
    #     new[label_dic[l]] = 1
        new_label.append(label_dic[l])

    # assert(len(new_label) == len(label))
    # print("Y shape: ",len(new_label[0]),len(new_label))
    return data,new_label




def load_data():
    print("Train Dev Data")
    train_dev_data = open(dataset_name + '.txt').readlines()
    train_dev_data_x,train_dev_data_y = preprocessing(train_dev_data)

    print("Test Data")
    test_data = open(dataset_name + '.t').readlines()
    test_x,test_y = preprocessing(test_data)

    return train_dev_data_x,train_dev_data_y,test_x,test_y


def main():
    print("in main")

    train_dev_x, train_dev_y, test_x , test_y = load_data()

    # train_x,train_y,dev_x,dev_y = train_test_split(train_dev_x,train_dev_y,test_size = 0.2,random_state = 10)
    # print(train_x.shape,train_y.shape,dev_x.shape,dev_y.shape)
    train_x = train_dev_x
    train_y = train_dev_y

    ss = StandardScaler()
    train_x = ss.fit_transform(train_x)
    test_x = ss.transform(test_x)

    t1 = time.time()

    lr = LogisticRegression() 
    lr.fit(train_x,train_y)
    # lr_y_predit = lr.predict(test_x ) 
    print("ALL Feature:")
    print ('Accuracy of LR Classifier:%f'%lr.score(test_x,test_y))

    t2 = time.time()

    print("time: ",t2 - t1)

    print("GBDT Feature:")

    print("Top 20: ")
    fgs = GBDTSelector()
    config = {}
    config['lgb_params'] = {'objective':'multiclass','num_class':num_class}
    config['eval_ratio'] = 0.05
    config['early_stopping_rounds'] = 10
    config['importance_type'] = 'split'
    config['num_boost_round'] = 10
    fgs.fit(train_x, train_y, config)
    
    important_feature = fgs.get_selected_features(need_feature)

    t3 = time.time()


    lr = LogisticRegression() 
    lr.fit(np.array(train_x)[:,important_feature],train_y)
    # lr_y_predit = lr.predict(test_x ) 
    
    print ('Accuracy of LR Classifier:%f'%lr.score(np.array(test_x)[:,important_feature],test_y))

    t4 = time.time()

    print('gbdt feature time: ',t3 - t2)
    print('gbdt lr time: ',t4 - t3)



    print("Gradient Feature:")
    print("Top 20: ")
    fgs = FeatureGradientSelector(n_epochs=5, n_features=need_feature)
    fgs.fit(train_x, train_y)
    
    important_feature = fgs.get_selected_features()

    t5 = time.time()

    # train_x = np.array(train_x)[:,important_feature]
    # test_x = np.array(test_x)[:,important_feature]
    lr = LogisticRegression() 
    lr.fit(np.array(train_x)[:,important_feature],train_y)
    # lr_y_predit = lr.predict(test_x ) 
    
    print ('Accuracy of LR Classifier:%f'%lr.score(np.array(test_x)[:,important_feature],test_y))

    t6 = time.time()
    print(important_feature)
    print('gradient feature time: ',t5 - t4)
    print('gradient lr time: ',t6 - t5)



if __name__ == "__main__":
    main()