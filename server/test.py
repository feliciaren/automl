'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-23 19:51:13
@LastEditors: feliciaren
@LastEditTime: 2020-02-24 08:57:29
'''
import tensorflow as tf
import numpy as np
import datetime
import argparse
import os
import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker 
import matplotlib


from examples.model import DNN
from search.grid_search import GridSearch
from search.bayesian_optimization import BayesianOptimization
from study import Study
from trials import Trials


os.environ['CUDA_VISIBLE_DEVICES'] = "1"
plt.switch_backend('agg')
save_dir = "./examples/data/"
test_dir = "./examples/data/"
json_dir = "./examples/"
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
          input_size = 9,
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

    # train_x = np.load(save_dir + 'x.npy')[:500,:9]
    # train_y = np.load(save_dir + 'y.npy')[:500,:]


    # eval_x = np.load(test_dir + 'x_test.npy')[:,:9]
    # eval_y = np.load(test_dir + 'y_test.npy')


    train_x = np.load(save_dir + 'x.npy')[:,:9]
    train_y = np.load(save_dir + 'y.npy')


    eval_x = np.load(test_dir + 'x_test.npy')[:,:9]
    eval_y = np.load(test_dir + 'y_test.npy')

    print('Train X size:',train_x.shape)
    print(len(train_y[0]))

    print('Eval X size:',eval_x.shape)

    
    study = Study.fromjson(json_dir + 'args.json')
    searcher = BayesianOptimization(study)
    trial_list = []
    loss = []
    for i in range(count):
        
        trial = searcher._get_next_trial(trials_list = trial_list,number = 1)
        print('Count: ',len(trial_list))
        
        losses = train(trial.params,train_x,train_y,eval_x,eval_y)
        metric = sum(losses[:-3]) + losses[-1] - losses[0]
        print('sum',sum(losses[:-3]))
        print(losses[-1] - losses[0])
        trial_list[-1].metric = metric
        print('Losses: ',metric)

        trial._info()

        loss.append(metric)
    
        with open('result','w',encoding='utf-8') as f:
            for i in range(len(loss)):
                f.write(str(loss[i]) + '\n')

main(10)