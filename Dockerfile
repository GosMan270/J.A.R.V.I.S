FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc portaudio19-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]