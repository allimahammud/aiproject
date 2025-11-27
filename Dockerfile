FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
# run alembic upgrade head on container start (optional)
CMD ["sh", "-c", "alembic upgrade head || true && uvicorn src.app.main:app --host 0.0.0.0 --port 8000"]
