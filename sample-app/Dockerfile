#sample Dockerfile with intentional mistakes,so that our PR safety checker has something real to catch

FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip curl
ENV API_KEY="test_Fake_key1234"
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]
#Issues on purpose:
#1.uses old and outdated base image
#2.Runs as root
#3.Installs packages without cleaning cache
#Hardcoding env credential

