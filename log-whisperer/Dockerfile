FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    nodejs npm curl bubblewrap socat ripgrep && \
    npm install -g @anthropic-ai/sandbox-runtime && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
