FROM ubuntu:focal-20200423

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    apache2 \
    bash \
    build-essential \
    libapache2-mod-wsgi-py3 \
    python3 \
    python3-dev\
    python3-pip \
    python3-mysqldb \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install virtualenv

ADD app /var/www/app

WORKDIR /var/www

RUN virtualenv venv

RUN . /var/www/venv/bin/activate

RUN pip install -r app/website/requirements.txt

RUN a2enmod wsgi

RUN cp /var/www/app/server/website.conf /etc/apache2/sites-available/website.conf

RUN mkdir -p /var/www/mywebsite/logs

RUN a2dissite 000-default.conf
RUN a2ensite website.conf

RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log
RUN ln -sf /proc/self/fd/1 /var/log/apache2/error.log

EXPOSE 80

WORKDIR /var/www/app

CMD  /usr/sbin/apache2ctl -D FOREGROUND
