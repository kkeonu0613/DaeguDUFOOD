# 1. Python 이미지를 베이스로 사용
FROM python:3.9-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

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
