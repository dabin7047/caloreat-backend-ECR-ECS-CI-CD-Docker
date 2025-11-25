# - C 확장 패키지들이 wheel이 없을 때를 대비해 빌드 도구만 둠
# - Postgres libpq 는 asyncpg에 필요 없으므로 설치하지 않음
FROM python:3.12-slim-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# C-확장 패키지 대비용 / wheel 빌드용 컴파일러 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# require 먼저 복사하고 설치하는 것이 가장 자주 쓰는 최적화 패턴
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# - 런타임에는 OS 패키지가 거의 필요 없음
# - libpq 계열 완전 제거 (requirements에 asyncpg만 있어서)
FROM python:3.12-slim-bookworm AS final

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# non-root 실행 (운영 보안)
RUN useradd -m app_user \
    && mkdir -p /app \
    && chown -R app_user:app_user /app

USER app_user
WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

ENV PATH="/home/app_user/.local/bin:${PATH}"

# 폴더구조 대로 루트 main.py + app/
COPY --chown=app_user:app_user app/ app/
COPY --chown=app_user:app_user main.py .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
