'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-11 14:01:36
@LastEditors: feliciaren
@LastEditTime: 2020-05-29 10:35:04
'''

import tensorflow as tf
import numpy as np
import datetime
import argparse
import os
import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker 
import matplotlib


from model import DNN
from server.search.grid_search import GridSearch
from server.search.bayesian_optimization import BayesianOptimization
from server.search.random_search import RandomSearch
# from server.search.cmaes import CmaesAlgorithm
from server.search.simulate_anneal import SimulateAnnealAlgorithm
from server.search.tpe import TpeAlgorithm
from server.search.evolution_search import EvolutionSearch
from server.search.hyperband_search import HyperBandSearch
from server.model.study import Study
from server.model.trials import Trials


os.environ['CUDA_VISIBLE_DEVICES'] = "3"
# os.environ['PYTHONPATH'] = '/data1/qspace/feliciaren/small/automl_2/automl/server'
plt.switch_backend('agg')
save_dir = "./data/"
test_dir = "./data/"
json_dir = "./"
epoch = 5


# batchGradient,Generates a batch iterator for a dataset.
def batch_iter(data, batch_size, num_epochs, shuffle=True):
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data)-1)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            if (batch_num + 1) * batch_size <= data_size:
                end_index = (batch_num + 1) * batch_size
                yield shuffled_data[start_index:end_index]
            else:
                end_index = data_size
                yield shuffled_data[start_index:end_index]  

def eval(sess,m,batch_size,x_eval,y_eval,summary_wt,step):
# 验证
    data = list(zip(x_eval,y_eval))
    batches = batch_iter(data,batch_size,1,False)
    losses = []
    predicts = []
    costs = []
    errors = []
    for batch in batches:
        inputs,targets = zip(*batch)
        predict,loss,summary,cost = m.eval(sess,inputs,targets)
        summary_wt.add_summary(summary, global_step = step)
        losses.append(loss)
        predicts.extend(predict)
        costs.extend(cost.mean(1).tolist())
        errors.extend(cost.tolist())
    return sum(losses)/len(losses),predicts,costs,np.array(errors).max(0).tolist()



def train(args,train_x,train_y,eval_x,eval_y):

    evaluate_step = int((len(train_y)-1)/args['batch_size']) + 1
    session_conf = tf.ConfigProto(allow_soft_placement=True,log_device_placement=False)
    session_conf.gpu_options.per_process_gpu_memory_fraction = 0.8

    print('evaluate_step:',evaluate_step)

    tf.reset_default_graph()

    DNNmodel = DNN(hidden_layer_size = args['hidden_layer_size'],
          depth = args['depth'],
          batch_size = args['batch_size'],
          input_size = 45,
          output_size = 6,
          learning_rate_base = args['lr'],
          moving_average_decay = 0.99,
          learning_rate_decay = args['lr_decay'],
          regularization_rate = args['regularization_rate'],
          evaluate_step = evaluate_step)
    
    with tf.Session(config=session_conf) as sess:

        summary_writer = tf.summary.FileWriter(logdir = save_dir + '/train', graph=sess.graph)
        summary_writer_eval = tf.summary.FileWriter(logdir = save_dir + '/eval', graph=sess.graph)

        sess.run(tf.global_variables_initializer())

        traindata = list(zip(train_x,train_y))
        batches = batch_iter(traindata, args['batch_size'], epoch)

        eval_errors = []

        losses = []

        for batch in batches:

            inputs,targets = zip(*batch)
            loss,step,summary = DNNmodel.train(sess,inputs,targets)

            if step % evaluate_step == 0:

                summary_writer.add_summary(summary, global_step = step)
                eval_step = int(step/evaluate_step)


                eval_loss,eval_predicts,eval_costs,eval_error = eval(sess,DNNmodel,args['batch_size'],eval_x,eval_y,summary_writer_eval,step)

                eval_errors.append(eval_error)
                time_str = datetime.datetime.now().isoformat()
                print(time_str ,'evaluate_step:',eval_step,'loss:',eval_loss)

                losses.append(eval_loss)
        return losses

def main(count = 10):

    # train_x = np.load(save_dir + 'x.npy')[:500,:]
    # train_y = np.load(save_dir + 'y.npy')[:500,:]


    # eval_x = np.load(test_dir + 'x_test.npy')[:500,:]
    # eval_y = np.load(test_dir + 'y_test.npy')[:500,:]


    train_x = np.load(save_dir + 'train_x.npy')
    train_y = np.load(save_dir + 'train_y.npy')


    eval_x = np.load(test_dir + 'test_x.npy')
    eval_y = np.load(test_dir + 'test_y.npy')

    print('Train X size:',train_x.shape)
    print(len(train_y[0]))

    print('Eval X size:',eval_x.shape)

    
    
    # searchers = [RandomSearch(),GridSearch(),BayesianOptimization(),TpeAlgorithm(),SimulateAnnealAlgorithm()]
    searchers = [RandomSearch()]
    # searcher = BayesianOptimization(study)
    f = open('metric_result','a+',encoding='utf-8')
    f2 = open('loss_result','a+',encoding='utf-8')
    for searcher in searchers:
        print(searcher.__class__)
        trials_list = []
        study = Study._from_json(json_dir + 'args1.json')
        loss = []
        eval_loss = []
        for i in range(count):
            
            trial = searcher._get_next_trial(study=study, trials_list = trials_list,number = 1)
            print('Count: ',len(trials_list))
            trials_list.extend([trial[0]])
            trial[0]._info()
            losses = train(trial[0].params,train_x,train_y,eval_x,eval_y)
            metric = sum(losses[-3:])
            print('sum',sum(losses[-3:]))
            # print(losses[-1] - losses[0])
            trials_list[-1].metric = metric
            trial[0]._info()
            print('Losses: ',metric)
            print('Final Losses', losses[-1])

            loss.append(metric)
            eval_loss.append(losses)
        

        f.write(str(searcher.__class__)+ '\n')
        for i in range(len(loss)):
            f.write(str(loss[i]) + '\n')

        f2.write(str(searcher.__class__)+ '\n')
        for i in range(len(eval_loss)):
            f2.write(str(eval_loss[i]) + '\n')

main(10)