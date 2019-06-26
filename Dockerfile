FROM python:3.7.3-stretch

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

EXPOSE 5000

# gunicorn app:app -k gevent -w 4
# CMD ["gunicorn", \
#     "app:app", \
#      "--bind", "0.0.0.0:8000", \
#      "-k","gevent", \
#     "-w", "4" ]

CMD ["pipenv", "run", "python3", "run.py"]