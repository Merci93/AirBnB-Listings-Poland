FROM apache/airflow:slim-latest
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --upgrade pip
USER airflow
WORKDIR /usr/local/airflow
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt
