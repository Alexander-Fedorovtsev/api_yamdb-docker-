FROM python:3.7-slim
COPY ./api_yamdb ./app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
WORKDIR /app
#CMD ["python3", "manage.py", "runserver", "0:8000"]
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:80", "--timeout", "240", "--workers=3", "--threads=3" ]

