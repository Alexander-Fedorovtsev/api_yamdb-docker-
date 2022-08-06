FROM python:3.7-slim
WORKDIR /app
COPY ./ /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
ENV PYTHONPATH "${PYTHONPATH}:/app/api_yamdb"
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:80", "--timeout", "240", "--workers=3", "--threads=3" ]

