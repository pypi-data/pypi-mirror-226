FROM docker.io/python:3.6.8-slim
ENV PYTHONUNBUFFERED 1
ENV http_proxy http://proxy.houston.hpecorp.net:8080/
ENV https_proxy http://proxy.houston.hpecorp.net:8080/
RUN apt-get update
RUN apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev

# For debugging purpose
RUN apt-get -y install vim

RUN pip3 install --upgrade pip

RUN mkdir -p /tmp/cmt

# Set the working directory
WORKDIR /tmp/cmt

# Copy the code
COPY cbt_map_transformer .

RUN ls /tmp/cmt

RUN pip3 install --no-cache-dir -r /tmp/cmt/requirements.txt

# unset proxy
ENV http_proxy=
ENV https_proxy=

EXPOSE 5000

ENTRYPOINT ["python3.6", "/tmp/cmt/server.py"]
