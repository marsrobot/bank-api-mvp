FROM ubuntu:focal-20200423

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 \
    python3-pip \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install virtualenv

WORKDIR /root

ADD . /root

RUN virtualenv venv

RUN . /root/venv/bin/activate

RUN pip install -r requirements.txt
