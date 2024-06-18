FROM python:3.10-slim
LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"
LABEL description="Slice KPI Calculator v1.0.0 for Open5GS"


RUN mkdir -p /exporter/

WORKDIR /exporter
COPY /app/requirements.txt ./
RUN pip install -r requirements.txt
COPY /app/* ./

EXPOSE 9000

CMD python3 kpi_calculator.py