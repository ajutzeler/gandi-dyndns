FROM python:2.7.12-alpine

MAINTAINER arnaud@kogikog.ch

WORKDIR /root

ADD docker/requirements.txt requirements.txt
ADD docker/run.py run.py
ADD docker/config-template.j2 config-template.j2
ADD gandi_dyndns.py gandi_dyndns.py
ADD providers.json providers.json

RUN pip install -r requirements.txt

CMD python run.py