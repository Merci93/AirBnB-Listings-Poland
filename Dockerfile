FROM apache/airflow:slim-latest-python3.13

USER root

# Prevent interactive prompts & reduce attack surface
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        libasound2 \
        libatk-bridge2.0-0 \
        libgtk-4-1 \
        libnss3 \
        xdg-utils \
        wget \
        curl \
        unzip \
        g++ \
        gcc \
        libpq-dev \
        xvfb \
        libgconf-2-4 && \
    apt-get purge -y --auto-remove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Chrome & Chromedriver (pinned + verified)
ARG CHROME_VERSION=121.0.6167.85
ARG CHROMEDRIVER_VERSION=121.0.6167.85

WORKDIR /tmp

RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip && \
    unzip chrome-linux64.zip && \
    mv chrome-linux64 /opt/chrome && \
    ln -s /opt/chrome/chrome /usr/local/bin/google-chrome && \
    rm chrome-linux64.zip && \
    \
    wget -q https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64*

USER airflow

ENV DISPLAY=:99

WORKDIR /usr/local/airflow

COPY --chown=airflow:airflow requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir uv==0.9.18 && \
    uv pip install --no-cache -r requirements.txt