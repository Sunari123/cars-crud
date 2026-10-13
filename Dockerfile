FROM python:3.12-slim

WORKDIR /app

RUN adduser --disabled-password --gecos '' appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /data
RUN chown -R appuser:appuser /app /data

USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]