FROM python:3.12-slim

WORKDIR /app

# Runtime defaults can still be overridden with -e at docker run time.
ENV APP_NAME="Visitor Logger" \
	PORT=5000 \
	LOG_FILE=/data/visits.log \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Ensure the persistent data path exists before the app starts.
RUN mkdir -p /data

EXPOSE 5000
VOLUME ["/data"]

CMD ["python", "app.py"]
