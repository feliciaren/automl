###
 # @Descripttion: 
 # @version: 
 # @Author: feliciaren
 # @Date: 2020-05-06 16:23:44
 # @LastEditors: feliciaren
 # @LastEditTime: 2020-05-06 20:16:00
 ###
#!/usr/bin/env bash
cd $(dirname $0)
version=$(cat ./server/model/version.py | grep '__version__ = ' | sed "s#__version__ = ##g" | sed "s#'##g")
img_name=automlservice
# cd ..
docker build ${EXTRA_BUILD_ARGS} . -t ${img_name}:${version} -t ${img_name}:latest

cat <<EOF
# You can use following commands to push images.
docker push ${img_name}:${version}
docker push ${img_name}:latest
EOF