# syntax=docker/dockerfile:1
FROM python:3.9-alpine
WORKDIR /server
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY reuquanrntes.txt requirements.txt
RUN pip install -r reuquanrntes.txt
EXPOSE 8000
COPY .. .
CMD ["flask", "run"]