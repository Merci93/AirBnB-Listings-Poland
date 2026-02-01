FROM apache/airflow:3.1.5

USER root

# Prevent interactive prompts & reduce attack surface
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        g++ \
        gcc \
        libpq-dev && \
    apt-get purge -y --auto-remove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow

WORKDIR /usr/local/airflow

COPY --chown=airflow:airflow requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir uv==0.9.18 && \
    uv pip install --no-cache -r requirements.txt