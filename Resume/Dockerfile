# syntax=docker/dockerfile:1
FROM python:3.11-slim-buster
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get -y update
RUN apt-get -y install git
# RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5001
COPY . .
CMD ["python3", "resume_api.py"]