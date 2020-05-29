###
 # @Descripttion: 
 # @version: 
 # @Author: feliciaren
 # @Date: 2020-05-06 16:10:33
 # @LastEditors: feliciaren
 # @LastEditTime: 2020-05-06 20:48:12
 ###

set -xe
cd $(dirname $0)

export PYTHONUNBUFFERED=1
PYTHONIOENCODING=utf-8 automlserver  --port=8686  2>&1 | tee ${LOG_PATH}/log
