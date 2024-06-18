FROM python:3.10-slim
LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"
LABEL description="Monitoring Manager v1.0.0 for Monarch"


RUN mkdir -p /monarch/

WORKDIR /monarch
COPY /app/requirements.txt ./
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    vim iputils-ping curl \
    && apt-get autoremove -y && apt-get autoclean
RUN pip install -r requirements.txt

# Install kubectl version 1.28.2
RUN curl -LO "https://storage.googleapis.com/kubernetes-release/release/v1.28.2/bin/linux/amd64/kubectl" \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl

COPY app /monarch/app
COPY run.py ./


EXPOSE 5000

CMD python3 run.py