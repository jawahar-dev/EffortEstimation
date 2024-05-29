FROM python:3.10-slim

# Set environment variables to prevent python from writing .pyc files and to buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
