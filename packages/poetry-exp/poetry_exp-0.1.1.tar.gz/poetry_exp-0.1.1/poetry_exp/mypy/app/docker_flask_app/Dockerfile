# docker build -t flask_app:v1 --build-arg http_proxy=http://web-proxy.sdc.hpecorp.net:8080 .
#  docker run -p 5001:5001 -d flask_app:v1
FROM python:3.8
ENV PYTHONUNBUFFERED 1
ARG PROXY_SERVER=$http_proxy

# RUN apt-get update

# Install all the requirements using pip
ADD requirements.txt requirements.txt
RUN pip3 install --proxy=$PROXY_SERVER -r requirements.txt

# App directory
ARG APP_ROOT_DIR=/usr/src/flask_app

# Prepare working directory
WORKDIR $APP_ROOT_DIR
ENV PYTHONPATH=$PYTHONPATH:$APP_ROOT_DIR

ADD ./app.py $APP_ROOT_DIR/app.py
EXPOSE 5001

ENTRYPOINT ["python3", "app.py"]
#ENTRYPOINT ["/bin/bash"]
