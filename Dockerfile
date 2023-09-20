FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install flask
RUN pip install Werkzeug

CMD ["python", "app.py"]