FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/jwt_auth

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]