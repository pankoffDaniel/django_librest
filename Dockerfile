FROM python:3.9.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -ms /bin/bash app

WORKDIR /django_librest

COPY . .

RUN apt-get update -y \
    && apt-get install ncat -y \
    && apt-get clean -y \
    && python -m pip install --upgrade pip \
	&& pip install -r requirements.txt \
	&& rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["./docker-entrypoint.sh"]
