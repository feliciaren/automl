'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-02-23 18:26:23
@LastEditors: feliciaren
@LastEditTime: 2020-05-19 19:02:49
'''
import tensorflow as tf 
import numpy as np 
from config import *
class DNN(object):
    def __init__(self,
        hidden_layer_size,
        depth,
        batch_size,
        input_size,
        output_size,
        learning_rate_base,
        learning_rate_decay,
        regularization_rate,
        moving_average_decay,
        evaluate_step
        ):

        self.hidden_layer_size = hidden_layer_size
        self.depth = depth
        self.batch_size = batch_size
        self.input_size = input_size
        self.output_size = output_size
        self.regularizer = tf.contrib.layers.l2_regularizer(regularization_rate)
        self.learning_rate_base = learning_rate_base
        self.learning_rate_decay = learning_rate_decay
        self.moving_average_decay = moving_average_decay
        self.evaluate_step = evaluate_step
        self.global_step = tf.Variable(0, name="global_step", trainable=False)
        self.build_model()
        

    def get_weight_variable(self,shape,regularizer,name):
        weights = tf.get_variable(name, shape, initializer = tf.truncated_normal_initializer(stddev = 0.01), dtype = tf.float64)
        if regularizer != None:
            tf.add_to_collection('losses',regularizer(weights))
        return weights

    def get_bias_variable(self,shape,name):
        biases = tf.get_variable(name,shape,initializer = tf.constant_initializer(0.0), dtype = tf.float64)
        return biases

    def build_model(self):
        print('building build_model...')

        self.inputs = tf.placeholder(tf.float64,[None,self.input_size],name = 'inputs')
        self.targets = tf.placeholder(tf.float64,[None,self.output_size],name = 'targets')
        

        with tf.variable_scope('Input_Layer'):
            weights = self.get_weight_variable([self.input_size,self.hidden_layer_size],self.regularizer,name = 'Input_Weights')
            biases = self.get_bias_variable([self.hidden_layer_size],'Input_Biases')
            layer1 = tf.nn.relu(tf.matmul(self.inputs,weights) + biases) 
            # tf.summary.histogram('Input_Weights',weights)
            # tf.summary.histogram('Input_Biases',biases)
            self.cur_layer = layer1

        for i in range(self.depth):
            with tf.variable_scope('Layer_'+str(i)):
                weights = self.get_weight_variable([self.hidden_layer_size,self.hidden_layer_size],self.regularizer,'Layer'+ str(i) + '_Weights')
                biases = self.get_bias_variable([self.hidden_layer_size],'Layer'+ str(i) + 'Biases')
                self.cur_layer = tf.nn.relu(tf.matmul(self.cur_layer,weights) + biases)
                # tf.summary.histogram('Layer'+ str(i) + 'Weights',weights)
                # tf.summary.histogram('Layer' + str(i) + 'Biases',biases)

        with tf.variable_scope('Output_Layer'):
            weights = self.get_weight_variable([self.hidden_layer_size,self.output_size],self.regularizer,'Output_Weights')
            biases = self.get_bias_variable([self.output_size],'Output_Biases')
            self.outputs = tf.matmul(self.cur_layer,weights) + biases
            # tf.summary.histogram('Output_Weights',weights)
            # tf.summary.histogram('Output_Biases',biases)

        variable_averages = tf.train.ExponentialMovingAverage(self.moving_average_decay,self.global_step)
        self.variable_averages_op = variable_averages.apply(tf.trainable_variables())

        with tf.variable_scope('Train'):



            # self.cost = tf.losses.mean_squared_error(self.targets,self.outputs)
            se = tf.square(self.targets-self.outputs)
            self.cost = tf.reduce_mean(se)
            tf.summary.scalar('Train_MSE',self.cost)
            # tf.summary.histogram('Train_MSE',self.cost)

            self.loss = self.cost + tf.add_n(tf.get_collection('losses'))
            tf.summary.scalar('Train_Loss',self.loss)
            # tf.summary.histogram('Train_Loss',self.loss)
            self.learning_rate = tf.train.exponential_decay(self.learning_rate_base,
                                                        self.global_step,
                                                        self.evaluate_step,
                                                        self.learning_rate_decay)
            optimizer = tf.train.AdamOptimizer(self.learning_rate)
            # optimizer = tf.train.GradientDescentOptimizer
            self.train_step = optimizer.minimize(self.loss,global_step = self.global_step)
            with tf.control_dependencies([self.train_step,self.variable_averages_op]):
                self.train_op = tf.no_op(name = 'train')

        with tf.variable_scope('Eval'):

            self.eval_cost = tf.abs(self.targets-self.outputs)
            self.eval_loss = tf.reduce_mean(tf.square(self.targets-self.outputs))
            tf.summary.scalar('Eval_Loss',self.eval_loss)
            # tf.summary.histogram('Eval_Loss',self.eval_loss)


        self.summary_op = tf.summary.merge_all()

    def train(self,sess,inputs,targets):
        input_feed = {self.inputs:inputs,
                    self.targets:targets}
        
        output_feed = [self.train_op,self.cost,self.global_step,self.summary_op]

        output = sess.run(output_feed,input_feed)

        return output[1],output[2],output[3]

    def eval(self,sess,inputs,targets):
        input_feed = {self.inputs:inputs,
        self.targets:targets}


        output_feed = [self.outputs,self.eval_loss,self.summary_op,self.eval_cost]


        predict = sess.run(output_feed,input_feed)
        

        return predict[0],predict[1],predict[2],predict[3]

    def save(self, sess, path, var_list=None, global_step=None):
        # var_list = None returns the list of all saveable variables
        saver = tf.train.Saver(var_list)

        # temporary code
        #del tf.get_collection_ref('LAYER_NAME_UIDS')[0]
        save_path = saver.save(sess, save_path=path, global_step=global_step)
        print('model saved at %s' % save_path)

    def restore(self, sess, path, var_list=None):
        # var_list = None returns the list of all saveable variables
        saver = tf.train.Saver(var_list)
        saver.restore(sess, save_path=path)
        print('model restored from %s' % path)


def test():

    hidden_layer_size = 512
    depth = 10
    batch_size = 2
    input_size = 9
    output_size = 6
    learning_rate_base = 1e-3
    learning_rate_decay = 0.99
    regularization_rate = 0.0001
    moving_average_decay = 0.99
    evaluate_step = 20

    inputs = (np.ones((2,9))).tolist()
    targets = (np.ones((2,6))).tolist()
    # targets = np.random.rand(2,6)
    print(type(inputs))
    print(type(targets))


    model = DNN(hidden_layer_size = hidden_layer_size,
        depth = depth,
        batch_size = batch_size,
        input_size = input_size,
        output_size = output_size,
        learning_rate_base = learning_rate_base,
        moving_average_decay = moving_average_decay,
        learning_rate_decay = learning_rate_decay,
        regularization_rate = regularization_rate,
        evaluate_step = evaluate_step)
    # print(model.layers)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for j in range(50):
            for i in range(20):
                # output = model.train(sess,inputs,targets)
                # print('step:',i,'loss:',output)
                loss,step,s1 = model.train(sess,inputs,targets)
                # print('step:',step,'loss:',loss)

            _,eval_loss,s2,eval_cost = model.eval(sess,inputs,targets)
            print('eval_loss:',eval_loss)
            print('eval_cost',eval_cost)





# test()

# def main():

    
#     train_x = np.load(save_dir + 'x.npy')
#     train_y = np.load(save_dir + 'y.npy')


#     eval_x = np.load(test_dir + 'x_test.npy')
#     eval_y = np.load(test_dir + 'y_test.npy')

#     print('Train X size:',train_x.shape)
#     print(len(train_y[0]))

#     print('Eval X size:',eval_x.shape)




