FROM docker.io/python:3.6.8-slim
ENV PYTHONUNBUFFERED 1
ENV http_proxy http://proxy.houston.hpecorp.net:8080/
ENV https_proxy http://proxy.houston.hpecorp.net:8080/
RUN apt-get update
RUN apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev

# For debugging purpose
RUN apt-get -y install vim

RUN pip3 install --upgrade pip

#RUN mkdir -p /tmp/cbt_map_transformer

# Set the working directory
WORKDIR /usr/local/lib/python3.6/site-packages

# Copy the code
COPY cbt_map_transformer/ /usr/local/lib/python3.6/site-packages/cbt_map_transformer/

RUN ls /usr/local/lib/python3.6/site-packages/cbt_map_transformer

RUN pip3 install --no-cache-dir -r /usr/local/lib/python3.6/site-packages/cbt_map_transformer/requirements.txt

#ENV PYTHONPATH "/tmp/cbt_map_transformer/"


# unset proxy
ENV http_proxy=
ENV https_proxy=

#EXPOSE 50051

ENTRYPOINT ["python3.6", "cbt_map_transformer/grpc_server.py"]

#ENTRYPOINT ["/bin/bash"]
