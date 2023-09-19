FROM python:3.10
WORKDIR /app
COPY requirements.txt .w
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["python", "main.py"]