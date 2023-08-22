FROM python:3.11.2-slim-bullseye AS app

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && apt install -y zlib1g-dev libjpeg-dev libpng-dev libpango-1.0-0 libpangoft2-1.0-0 libopenjp2-7-dev libffi-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && useradd --create-home python \
  && chown python:python -R /app \
  && mkdir /static \
  && chown python:python -R /static

USER python

# Copy local django/ contents to container /app (WORKDIR)
COPY --chown=python:python . .


ENV PYTHONUNBUFFERED="true" \
    PYTHONPATH="/app" \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python" \
    DJANGO_SETTINGS_MODULE="jornada.settings"


RUN python -m pip install --upgrade pip
RUN python -m pip install /app