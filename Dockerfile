FROM python:3.11-slim

WORKDIR /src

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    git \
    curl \
    wget

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
