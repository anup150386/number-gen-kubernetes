## Dockerfile
#
## Use an official Python runtime as a parent image
#FROM python:3.10-slim
#
## Set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#
## Install dependencies
#COPY requirements.txt requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
#
## Copy the rest of the project files
#COPY . /app/
#WORKDIR /app
#
#
#
## Expose the app's port
#EXPOSE 8000
#
## Run the Django server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls -a

EXPOSE 8000

CMD ["python", "number_gen/manage.py", "runserver", "0.0.0.0:8000"]
