###
 # @Descripttion: 
 # @version: 
 # @Author: feliciaren
 # @Date: 2020-05-06 16:11:14
 # @LastEditors: feliciaren
 # @LastEditTime: 2020-05-06 21:33:02
 ###
#!/usr/bin/env bash
curl -XPOST --data '{"goal":"MAXIMIZE","maxTrials":"5","params":[{"parameterName": "hidden","type": "DISCRETE","feasiblePoints": [8,16,32],"scalingType": "LINEAR"}]}' localhost:8686


