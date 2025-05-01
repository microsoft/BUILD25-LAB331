FROM  python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--reload"]
