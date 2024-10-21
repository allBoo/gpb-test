FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
  postgresql-client \
  libpq-dev \
  pkg-config \
  g++ \
  wget \
  git \
  curl \
  gcc \
  libc6-dev


COPY . /app/
WORKDIR /app/

RUN pip install -r requirements.txt
