FROM python:3.10-slim
LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"
LABEL description="Request Translator v1.0.0 for Monarch"


RUN mkdir -p /monarch/

WORKDIR /monarch
COPY /app/requirements.txt ./
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    vim iputils-ping curl \
    && apt-get autoremove -y && apt-get autoclean
RUN pip install -r requirements.txt

COPY app /monarch/app
COPY run.py ./


EXPOSE 5000

CMD python3 run.py