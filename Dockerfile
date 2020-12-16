FROM python:3.7-alpine

ENV HTTPS_PROXY="http://10.1.40.10:8908"

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app
COPY . .
CMD ["main.py"]
ENTRYPOINT ["python3"]

