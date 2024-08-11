FROM apache/airflow:slim-latest-python3.9

USER root

RUN apt-get update -qq -y && \
    apt-get install -y \
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
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q -O chrome-linux64.zip https://bit.ly/chrome-linux64-121-0-6167-85 && \
    unzip chrome-linux64.zip && \
    rm chrome-linux64.zip && \
    mv chrome-linux64 /opt/chrome/ && \
    ln -s /opt/chrome/chrome /usr/local/bin/ && \
    wget -q -O chromedriver-linux64.zip https://bit.ly/chromedriver-linux64-121-0-6167-85 && \
    unzip -j chromedriver-linux64.zip chromedriver-linux64/chromedriver && \
    rm chromedriver-linux64.zip && \
    mv chromedriver /usr/local/bin/

RUN python -m pip install --upgrade pip

USER airflow

ENV DISPLAY=:99

WORKDIR /usr/local/airflow

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
