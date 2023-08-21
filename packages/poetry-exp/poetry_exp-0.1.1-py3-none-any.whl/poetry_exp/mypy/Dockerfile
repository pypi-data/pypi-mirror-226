# First delete all pycache
# find . -type d -name __pycache__ -exec rm -r {} \+
# docker build -t aafak/mypy:v3 --build-arg http_proxy=http://web-proxy.sdc.hpecorp.net:8080 .
# sudo docker run -p 5001:5001 -d aafak/mypy:v3
# sudo docker exec -it a92c1b4c02e328c576250da974a6b6ed7a12de6a81dff8c85ee996164ebb8f49 /bin/bash
# For pushing
# sudo docker push aafak/mypy:v3

FROM python:3.8
ENV PYTHONUNBUFFERED 1
ARG PROXY_SERVER=$http_proxy

# RUN apt-get update

# Install all the requirements using pip
ADD requirements.txt requirements.txt
ADD Dockerfile Dockerfile

RUN pip3 install --proxy=$PROXY_SERVER -r requirements.txt

# App directory
ARG APP_ROOT_DIR=/usr/src/mypy

# Prepare working directory
WORKDIR $APP_ROOT_DIR
ENV PYTHONPATH=$PYTHONPATH:$APP_ROOT_DIR

COPY ./__init__.py $APP_ROOT_DIR/__init__.py
COPY ./app $APP_ROOT_DIR/app
EXPOSE 5001

ENTRYPOINT ["python3", "app/main.py"]
#ENTRYPOINT ["/bin/bash"]
