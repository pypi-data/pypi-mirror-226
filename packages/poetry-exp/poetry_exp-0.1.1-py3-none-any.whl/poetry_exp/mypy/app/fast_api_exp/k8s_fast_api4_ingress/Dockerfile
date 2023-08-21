# (k8s_fast_api_venv) aafak@aafak-rnd-vm:~/k8s_apps/k8s_fast_api$ sudo docker build -t fastapi_app:v1 --build-arg http_proxy=http://web-proxy.sdc.hpecorp.net:8080 .

from python:3.8
ARG PROXY_SERVER=$http_proxy

ADD requirements.txt requirements.txt

RUN pip3 install --proxy=$PROXY_SERVER -r requirements.txt

ARG APP_ROOT_DIR=/usr/src/k8sFastApiApp
WORKDIR $APP_ROOT_DIR

ENV PYTHONPATH=$PYTHONPATH:$APP_ROOT_DIR

ADD ./app/* $APP_ROOT_DIR/

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host",  "0.0.0.0", "--port", "8000"]
