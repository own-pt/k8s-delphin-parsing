FROM python:3.7-alpine 

RUN pip install requests redis rq

WORKDIR /root/

COPY init.py settings.py ./

CMD python3 init.py
