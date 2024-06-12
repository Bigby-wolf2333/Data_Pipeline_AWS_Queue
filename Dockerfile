FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Install AWS CLI
RUN apt-get update && apt-get install -y awscli

CMD ["python", "main.py"]
