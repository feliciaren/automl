###
 # @Descripttion: 
 # @version: 
 # @Author: feliciaren
 # @Date: 2020-05-06 16:11:14
 # @LastEditors: feliciaren
 # @LastEditTime: 2020-05-29 15:58:32
 ###
#!/usr/bin/env bash
curl -XPOST --data '{"goal":"MAXIMIZE","maxTrials":"5","params":[{"parameterName": "hidden","type": "DISCRETE","feasiblePoints": [8,16,32],"scalingType": "LINEAR"}]}' localhost:8686

wait

curl -XPOST --data '{"name": " _590ba019-2277-3e9c-a43c-f9142262c260", "params": [{"parameterName": "hidden", "type": "DISCRETE", "feasiblePoints": [8, 16, 32], "scalingType": "LINEAR"}, {"parameterName": "optimizer", "type": "CATEGORICAL", "feasiblePoints": ["sgd", "adagrad"], "scalingType": "LINEAR"}, {"parameterName": "batch_normalization", "type": "CATEGORICAL", "feasiblePoints": ["true", "false"], "scalingType": "LINEAR"}, {"parameterName": "learning_rate", "type": "DOUBLE", "minValue": 0.01, "maxValue": 0.5, "scalingType": "LINEAR"}], "create_time": 1590738299.817953, "update_time": 1590738299.817953, "goal": "MAXIMIZE", "trials_list": [], "number": 1}' localhost:8686