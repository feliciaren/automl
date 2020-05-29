HIDDEN_LAYER_SIZE = 512
DEPTH = 10
GPU = 1
# =================
BATCH_SIZE = 256
# ================
INPUT_SIZE = 9
MULTI_INPUT_SIZE = 45
OUTPUT_SIZE = 6
LR = 0.00003
LR_DECAY = 0.99
REGULARIZATION_RATE = 0.0001
MOVING_AVERAGE_DECAY = 0.99
ACTIVATE_FUNCTION = 'relu'
# ===================
EPOCH = 500
IS_TRAIN = False
# =================

data_dir = './data/data_m/'
result_dir = './result/'
log_dir = './log/'

allow_soft_placement = True
log_device_placement = False
