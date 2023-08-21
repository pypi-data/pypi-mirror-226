FROM python:3.8
ENV PYTHONUNBUFFERED 1
ARG PROXY_SERVER=$http_proxy

RUN apt-get update

# Install all the requirements using pip
ADD requirements.txt requirements.txt
RUN pip3 install --proxy=$PROXY_SERVER -r requirements.txt

# For debugging purpose
RUN apt-get -y install vim

# App directory
ARG APP_ROOT_DIR=/usr/src/cbt-map-transformer

# Prepare working directory
WORKDIR $APP_ROOT_DIR
ENV PYTHONPATH=$PYTHONPATH:$APP_ROOT_DIR

COPY ./app $APP_ROOT_DIR/app
COPY docker-entrypoint.sh /usr/local/bin/

#RUN python3 -m pip3 install --proxy=$PROXY_SERVER -r requirements.txt

RUN cd $APP_ROOT_DIR && python3 -m grpc_tools.protoc -I . --python_out=. \
    --grpc_python_out=. app/grpc_lib/protos/*/*/*.proto

EXPOSE 5001

RUN rm -f $APP_ROOT_DIR/requirements.txt
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]