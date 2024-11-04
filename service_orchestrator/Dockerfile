FROM python:3.10-slim
LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"
LABEL description="Dummy Service Orchestrator v1.0.0 for Monarch"

# Install curl, vim
RUN apt-get update && \
    apt-get install -y curl vim && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /service_orchestrator/

WORKDIR /service_orchestrator
COPY /app/requirements.txt ./
RUN pip install -r requirements.txt
COPY /app/* ./

EXPOSE 5001

CMD ["python3", "run.py"]