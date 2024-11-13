FROM python:3.10-slim
LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"
LABEL description="Rogers Workshop v1.0"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install iproute2 iputils-ping curl -y \
    && apt-get install vim nano iperf3 net-tools tcpdump -y \
    && apt-get clean

RUN mkdir -p /workshop/
WORKDIR /workshop
COPY /app/requirements.txt ./
RUN pip install -r requirements.txt
COPY /app/* ./

EXPOSE 8000

CMD ["python3", "exporter.py"]