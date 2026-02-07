FROM python:3.12-slim

WORKDIR /app

# (선택) 빌드 속도/캐시를 위해 requirements 먼저 복사
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 코드 복사
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
