# docker build -t api_server:v1 --build-arg http_proxy=http://web-proxy.sdc.hpecorp.net:8080 .
#  docker run -p 5003:5003 -d --name api_server --net my_network api_server:v1
FROM python:3.8
ENV PYTHONUNBUFFERED 1
ARG PROXY_SERVER=$http_proxy

# RUN apt-get update

# Install all the requirements using pip
ADD requirements.txt requirements.txt
RUN pip3 install --proxy=$PROXY_SERVER -r requirements.txt

# App directory
ARG APP_ROOT_DIR=/usr/src/api_server

# Prepare working directory
WORKDIR $APP_ROOT_DIR
ENV PYTHONPATH=$PYTHONPATH:$APP_ROOT_DIR

ADD ./api_server.py $APP_ROOT_DIR/api_server.py
EXPOSE 5003

ENTRYPOINT ["python3", "api_server.py"]
#ENTRYPOINT ["/bin/bash"]
