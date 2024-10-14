#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # 기본적으로 'dufood.settings' 설정 파일을 사용
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dufood.settings')  # 기본 설정

    # 배포 환경일 경우, settings.production을 사용하도록 설정
    if os.environ.get('DJANGO_ENV') == 'production':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'dufood.settings.production'  # 배포용 설정

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
