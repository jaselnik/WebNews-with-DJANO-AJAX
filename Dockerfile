FROM python:3

ARG requirements=requirements/production.txt

RUN mkdir src/
COPY requirements/ src/
WORKDIR /src/
ADD . /src/
RUN pip install -r $requirements
