FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src
COPY src/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app","--app-dir", "src" ,"--host", "0.0.0.0", "--port", "8002"]
