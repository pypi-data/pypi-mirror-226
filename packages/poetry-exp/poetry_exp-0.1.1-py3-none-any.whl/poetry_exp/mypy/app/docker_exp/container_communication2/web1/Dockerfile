# docker build -t flask_app1:v1 --build-arg http_proxy=http://web-proxy.sdc.hpecorp.net:8080 .
#  docker run -p 5002:5002 -d flask_app1:v1  --network=host
FROM python:3.8
ENV PYTHONUNBUFFERED 1
ARG PROXY_SERVER=$http_proxy

# RUN apt-get update

# Install all the requirements using pip
ADD requirements.txt requirements.txt
RUN pip3 install --proxy=$PROXY_SERVER -r requirements.txt

# App directory
ARG APP_ROOT_DIR=/usr/src/flask_app1

# Prepare working directory
WORKDIR $APP_ROOT_DIR
ENV PYTHONPATH=$PYTHONPATH:$APP_ROOT_DIR

ADD ./app1.py $APP_ROOT_DIR/app1.py
EXPOSE 5002

ENTRYPOINT ["python3", "app1.py"]
#ENTRYPOINT ["/bin/bash"]
