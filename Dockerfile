FROM python:3.10

ENV PYTHONUNBUFFERED 1

ENV APP_ROOT /app

WORKDIR ${APP_ROOT}

RUN apt-get update

RUN apt-get install -y python3.10-dev python3.10-pip default-libmysqlclient-dev

RUN pip3 install -U pip

COPY requirements.txt ${APP_ROOT}/requirements.txt

RUN pip3 install -r ${APP_ROOT}/requirements.txt

# Set the working directory to /app
WORKDIR ${APP_ROOT}

# Set environment = prod
ENV ENVIRONMENT prod

# Copy the current directory contents into the container at /app
ADD ./src/ ${APP_ROOT}

CMD ls -la ${APP_ROOT}

RUN chmod 775 -R ${APP_ROOT}

CMD gunicorn -w 5 -t 90 -b 0.0.0.0:8000 server_config.wsgi:application
