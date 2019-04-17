FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3-minimal \
        python3-pip

# We copy just the requirements.txt first to leverage Docker cache
# COPY ./requirements.txt /app/requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

WORKDIR /app

RUN pip3 install pipenv
RUN pipenv install

COPY . /app

WORKDIR /app

# gunicorn app:app -k gevent -w 4
# CMD ["gunicorn", \
#     "app:app", \
#      "--bind", "0.0.0.0:8000", \
#      "-k","gevent", \
#     "-w", "4" ]

CMD ["pipenv", "run", "python3", "run.py"]
# RUN pipenv run python3 run.py
# ENTRYPOINT [ "python3" ]

# CMD [ "run.py" ]
