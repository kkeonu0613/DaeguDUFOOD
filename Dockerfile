# 1. Python 이미지를 베이스로 사용
FROM python:3.9-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 시스템 패키지 설치 (필요한 경우)
# 예를 들어, Pillow 설치에 필요한 라이브러리가 있을 수 있습니다.
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. 필수 의존성 파일을 복사
COPY requirements.txt /app/

# 5. 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 6. 프로젝트 파일들을 복사
COPY . /app/

# 7. 데이터베이스 마이그레이션 실행 (필요할 경우)
RUN python manage.py migrate --noinput

# 8. 정적 파일을 수집 (필요할 경우)
RUN python manage.py collectstatic --noinput

# 9. Gunicorn을 통해 애플리케이션 실행
CMD ["gunicorn", "dufood.wsgi:application", "--bind", "0.0.0.0:8000"]
