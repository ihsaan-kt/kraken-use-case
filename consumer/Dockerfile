FROM python:3.9-slim
WORKDIR /app
# Copy from project root (../requirements.txt)
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pulsar_consumer.py .
CMD ["python", "pulsar_consumer.py"]