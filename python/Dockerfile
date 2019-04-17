FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev wget git vim \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN pip3 install progressbar spacy regex pandas nltk pandas-gbq sklearn pybind11 scipy redis nltk unidecode

#RUN git clone https://github.com/facebookresearch/fastText.git \
#	&& cd fastText \
#	&& pip3 install . \
#	&& cd ..

ADD script.py /

