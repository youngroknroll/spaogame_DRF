# Stage 1: Builder
FROM python:3.13-slim AS builder

# UV 설치
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY pyproject.toml uv.lock ./

# 의존성 설치
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM python:3.13-slim

# 시스템 패키지 설치 (PostgreSQL 클라이언트)
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# Builder에서 가상환경 복사
COPY --from=builder /app/.venv /app/.venv

# 소스 코드 복사
COPY . .

# 환경변수 설정
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"

# Entrypoint 스크립트 실행
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# 기본 명령어
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
