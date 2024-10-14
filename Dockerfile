# 1. Python 이미지를 베이스로 사용
FROM python:3.10-slim AS python-base

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필수 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 4. 프로젝트 파일들을 복사
COPY . /app/

# 5. 데이터베이스 마이그레이션 실행
RUN python manage.py migrate --noinput

# 6. 정적 파일을 수집
RUN python manage.py collectstatic --noinput

# Nginx 설정을 위한 별도의 베이스 사용
FROM nginx:stable-alpine AS nginx-base

# Nginx 설정 복사
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Python에서 수집한 정적 파일 복사
COPY --from=python-base /app/staticfiles /usr/share/nginx/html/static

# Nginx 시작
CMD ["nginx", "-g", "daemon off;"]
