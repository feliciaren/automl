FROM pytorch/pytorch:1.0.1-cuda10.0-cudnn7-runtime
RUN apt-get update && apt-get install -y jq curl xz-utils htop && rm -rf /var/lib/apt/lists/*
COPY . /src/automlclient
RUN python3 -m pip install /src/automlclient
RUN rm -rf /src/automl-server
ENV LOG_PATH /log
EXPOSE 8686
WORKDIR /
