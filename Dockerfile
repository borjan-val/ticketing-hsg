FROM python:3.13.1-bookworm
COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD gunicorn -w $WORKERS -b 0.0.0.0:80 app:app