FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        curl \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /home/base-rag-chatbot

COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .