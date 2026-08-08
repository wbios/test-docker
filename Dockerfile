FROM python:3.14-slim

WORKDIR /app

RUN pip install flask psycopg2-binary

COPY app.py .
COPY templates templates

EXPOSE 80

CMD ["python", "app.py"]
