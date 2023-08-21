# docker build -t db_server:v1 --build-arg http_proxy=http://web-proxy.sdc.hpecorp.net:8080 .
#  docker run -p 5002:5002 -d --name db_server db_server:v1
FROM python:3.8
ENV PYTHONUNBUFFERED 1
ARG PROXY_SERVER=$http_proxy

# RUN apt-get update

# Install all the requirements using pip
ADD requirements.txt requirements.txt
RUN pip3 install --proxy=$PROXY_SERVER -r requirements.txt

# App directory
ARG APP_ROOT_DIR=/usr/src/db_server

# Prepare working directory
WORKDIR $APP_ROOT_DIR
ENV PYTHONPATH=$PYTHONPATH:$APP_ROOT_DIR

ADD ./db_server.py $APP_ROOT_DIR/db_server.py
EXPOSE 5002

ENTRYPOINT ["python3", "db_server.py"]
#ENTRYPOINT ["/bin/bash"]
