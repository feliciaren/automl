'''
@Descripttion: 
@version: 
@Author: feliciaren
@Date: 2020-05-12 15:01:08
@LastEditors: feliciaren
@LastEditTime: 2020-05-12 15:01:57
'''
DOUBLE = "double"
INTEGRAL = "integral"
NAN = "nan"
STRING = "string"

REGRESSION = 'regression'
BINARY_CLASSIFICATION = 'binary_classification'
MULTICLASS_CLASSIFICATION = 'multiclass_classification'
CLASSIFICATION_TASKS = [BINARY_CLASSIFICATION, MULTICLASS_CLASSIFICATION]
SUPERVISED_TASKS = [BINARY_CLASSIFICATION, MULTICLASS_CLASSIFICATION, REGRESSION]

F1 = 'f1'
accuarcy = 'accuracy'
precision = 'precision'
recall = 'recall'

TASK = 'task'
MULTICLASS = 'multiclass'
CATEGORY_COLS = 'category_cols'
CONTINUAL_COLS = 'continual_cols'
LABEL_COL = 'label_col'

MAX_BIN = 'max_bin'
MAX_FEATURE_NUM = 'max_feature_num'