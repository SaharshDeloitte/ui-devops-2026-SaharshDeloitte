FROM python:latest

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV PORT=8000

EXPOSE 5000

CMD ["python", "app.py"]
