FROM apache/airflow:slim-latest-python3.9
USER root
RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends g++ gcc libpq-dev && \ 
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --upgrade pip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && \
    apt-get -y install google-chrome-stable
USER airflow
WORKDIR /usr/local/airflow
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
