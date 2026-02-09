#!/bin/bash
set -e

echo "Waiting for database..."
python << END
import sys
import time
import psycopg

max_retries = 30
retry_interval = 1

for i in range(max_retries):
    try:
        conn = psycopg.connect(
            dbname="${POSTGRES_DB:-spaogame}",
            user="${POSTGRES_USER:-spaogame}",
            password="${POSTGRES_PASSWORD:-spaogame_password}",
            host="${DB_HOST:-db}",
            port="${DB_PORT:-5432}"
        )
        conn.close()
        sys.exit(0)
    except Exception:
        print(f"Database connection failed. Retrying... ({i+1}/{max_retries})")
        time.sleep(retry_interval)

print("Failed to connect to database after maximum retries.")
sys.exit(1)
END

echo "Database is ready!"

# 마이그레이션 실행
echo "Running migrations..."
python manage.py migrate --noinput

# Static 파일 수집 (운영 환경)
if [ "$DEBUG" = "False" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# 슈퍼유저 생성 (개발 환경, 환경변수로 제어)
if [ "$CREATE_SUPERUSER" = "True" ]; then
    echo "Creating superuser..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@spaogame.com').exists():
    User.objects.create_superuser(
        email='admin@spaogame.com',
        password='admin',
        name='Admin User'
    )
    print('Superuser created: admin@spaogame.com / admin')
END
fi

echo "Starting application..."
exec "$@"
