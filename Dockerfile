FROM python:3.11

# Install Java
RUN apt-get update && apt-get install -y \
    default-jdk

# Install C++ (g++)
RUN apt-get install -y \
    g++

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000


CMD  ["python", "manage.py", "runserver","0.0.0.0:8000"]

