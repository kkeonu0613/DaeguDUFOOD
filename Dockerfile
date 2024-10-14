# 1. Python과 Nginx 이미지를 함께 사용
FROM python:3.10-slim AS python-base
FROM nginx:stable-alpine AS nginx-base

# 2. Python 설치 및 작업 디렉토리 설정
WORKDIR /app

# 3. 필수 의존성 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 4. 프로젝트 파일 복사
COPY . /app/

# 5. 데이터베이스 마이그레이션 및 정적 파일 수집
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

# 6. Nginx 설정 복사 및 정적 파일을 Nginx에서 서빙
COPY nginx/default.conf /etc/nginx/conf.d/

# 7. Gunicorn으로 Django 애플리케이션 실행
CMD ["gunicorn", "dufood.wsgi:application", "--bind", "0.0.0.0:8000", "--log-level", "info"]
