FROM ubuntu:latest

WORKDIR /root/

RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y unzip curl openssh-client git sbcl supervisor \
	python3-dev python3-pip

RUN curl -O http://sweaglesw.org/linguistics/ace/download/ace-0.9.30-x86-64.tar.gz && \
	tar xzf ace-0.9.30-x86-64.tar.gz && \
	rm ace-0.9.30-x86-64.tar.gz

RUN curl -O http://sweaglesw.org/linguistics/ace/download/erg-2018-x86-64-0.9.30.dat.bz2 && \
	bzip2 -d erg-2018-x86-64-0.9.30.dat.bz2

RUN  curl -O http://beta.quicklisp.org/quicklisp.lisp

RUN pip3 install --upgrade pip && \
	pip install requests rq pydelphin

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH="/root/ace-0.9.30/:$PATH"
ENV ERG_DAT=/root/erg-2018-x86-64-0.9.30.dat

COPY settings.py /root/
