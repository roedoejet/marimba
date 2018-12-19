# Base Image
FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive

COPY . / marimba/

# Get dependencies
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python-dev build-essential
RUN apt-get install -y nano git-all
RUN apt-get install -y libfftw3-dev libsndfile1-dev libao-dev libsamplerate0-dev libncurses5-dev libncursesw5-dev libgtk2.0-dev
RUN pip3 install -r marimba/requirements.txt
RUN git clone https://github.com/kichiki/WaoN.git

RUN cd WaoN && make

RUN cd marimba && pip3 install -e .

WORKDIR /

CMD gunicorn marimba:app --bind 0.0.0.0:$PORT