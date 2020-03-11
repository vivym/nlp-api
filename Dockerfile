FROM python:3.7

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN python setup.py install

EXPOSE 12377

ENTRYPOINT ["python", "-m", "nlp.server"]
