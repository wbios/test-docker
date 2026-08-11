FROM python:3.14-slim

WORKDIR /app

RUN pip install flask psycopg2-binary pytest

COPY app.py .
COPY db.py .
COPY test_app.py .
COPY templates templates

EXPOSE 80

CMD ["python", "app.py"]
