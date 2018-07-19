FROM python:3
RUN mkdir src/
COPY requirements.txt src/
WORKDIR /src/
RUN pip install -r requirements.txt
ADD . /src/
