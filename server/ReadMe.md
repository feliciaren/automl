<!--
 * @Descripttion: 
 * @version: 
 * @Author: feliciaren
 * @Date: 2020-05-19 19:31:34
 * @LastEditors: feliciaren
 * @LastEditTime: 2020-05-29 15:52:35
--> 


# 自动机器学习系统


## 框架结构

本系统包含多个模块。主体部分是自动特征工程、自动调优、自动早停三个模块。本框架基本的结构如下所示：

```
----server\ ： 源码目录
    |----early_stop ： 自动早停
    |----examples : 自动特征工程算例
    |----feature_select ： 自动特征工程
    |----model ： 系统主体
    |----search ： 自动调优算法
    |----testtools： 测试合集

```

## 使用方法

1. build docker:

```
    sh build_docker.sh

```

2. 启动服务

```
    docker run -it -p 8686:8686 automlservice:latest /bin/bash
    sh server.sh
```

3. 测试

```
    sh liveness_prob.sh
```