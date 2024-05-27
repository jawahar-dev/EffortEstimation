FROM python:3.9-slim

WORKDIR /effort-app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . /effort-app

# Make port 5000 available to the world outside this container
EXPOSE 5000

CMD ["python3", "run.py"]
