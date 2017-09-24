FROM python:2.7-slim
LABEL maintainer "https://hub.docker.com/u/pceric/"
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "-u", "dyndns53.py"]
