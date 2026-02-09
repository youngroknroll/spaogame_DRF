# Spaogame API

![CI](https://github.com/youngroknroll/spaogame_DRF/workflows/CI/badge.svg)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-6.0.1-green.svg)](https://www.djangoproject.com/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Django REST Framework 기반의 전자상거래 플랫폼 API 서버

## 📋 목차

- [개요](#개요)
- [기술 스택](#기술-스택)
- [프로젝트 구조](#프로젝트-구조)
- [빠른 시작 (Docker)](#빠른-시작-docker)
- [설치 및 실행](#설치-및-실행)
- [데이터베이스 구조](#데이터베이스-구조)
- [주요 기능](#주요-기능)
- [API 문서](#api-문서)
- [개발 가이드](#개발-가이드)
- [CI/CD](#cicd)

## 개요

**Spaogame API**는 사용자 인증, 상품 관리, 장바구니, 주문, 게시판 등의 기능을 제공하는 REST API 서버입니다.

**주요 특징:**
- JWT 기반 사용자 인증
- 다양한 상품 카테고리 관리 (메뉴/카테고리 계층)
- 색상/사이즈 조합을 통한 상품 상세 정보 관리
- 장바구니 및 위시리스트 관리
- 게시판 및 댓글 기능
- 포괄적인 데이터 검증 및 무결성 제약

## 기술 스택

| 카테고리 | 기술 |
|--------|------|
| **프레임워크** | Django 6.0.1, Django REST Framework 3.16.1 |
| **인증** | SimpleJWT 5.5.1 |
| **문서화** | drf-spectacular 0.29.0 |
| **필터링** | django-filter 25.2 |
| **데이터베이스** | PostgreSQL 17 (운영), SQLite (개발) |
| **캐시/메시지** | Redis 7 |
| **비밀번호 해싱** | Argon2 |
| **환경 설정** | python-dotenv 1.2.1, dj-database-url 3.1.0 |
| **테스팅** | pytest 9.0.2, pytest-django 4.11.1, pytest-cov 7.0.0 |
| **코드 품질** | Ruff 0.15.0, pre-commit 4.5.1 |
| **컨테이너** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **WSGI 서버** | Gunicorn 25.0.3 (운영) |
| **Python** | 3.13+ |
| **패키지 관리** | UV (Astral) |

## 프로젝트 구조

```
spaogame-api/
├── apps/                          # Django 앱들
│   ├── core/                      # 핵심 모델 (TimeStampedModel 등)
│   ├── users/                     # 사용자 인증 및 관리
│   │   ├── models.py             # User 모델
│   │   ├── views.py              # 회원가입, 로그인, 프로필 API
│   │   ├── serializers.py        # 사용자 시리얼라이저
│   │   ├── tests/                # 사용자 관련 테스트
│   │   └── migrations/           # 마이그레이션 파일
│   ├── products/                  # 상품 관리
│   │   ├── models.py             # Menu, Category, Product, DetailedProduct 등
│   │   ├── views.py              # 상품 조회, 검색, 필터링
│   │   ├── serializers.py        # 상품 시리얼라이저
│   │   ├── tests/                # 상품 관련 테스트
│   │   └── migrations/
│   ├── orders/                    # 주문 및 장바구니
│   │   ├── models.py             # Cart, CartItem, Wishlist 모델
│   │   ├── views.py              # 장바구니, 주문 관리 API
│   │   ├── serializers.py        # 주문 시리얼라이저
│   │   ├── tests/                # 장바구니 테스트
│   │   └── migrations/
│   └── postings/                  # 게시판 및 댓글
│       ├── models.py             # Posting, Comment 모델
│       ├── views.py              # 게시판 API
│       ├── serializers.py        # 게시판 시리얼라이저
│       ├── tests/                # 게시판 테스트
│       └── migrations/
├── config/                        # 프로젝트 설정
│   ├── settings.py               # Django 설정 (환경변수 기반)
│   ├── urls.py                   # 루트 URL 라우팅
│   ├── asgi.py                   # ASGI 설정
│   └── wsgi.py                   # WSGI 설정
├── conftest.py                   # pytest 글로벌 설정
├── pytest.ini                    # pytest 설정
├── pyproject.toml                # 프로젝트 메타데이터 및 의존성
├── uv.lock                       # UV 의존성 잠금 파일
├── manage.py                     # Django 관리 스크립트
├── main.py                       # 진입점
├── Dockerfile                    # Docker 이미지 빌드 설정
├── docker-compose.yml            # Docker Compose 설정
├── docker-entrypoint.sh          # 컨테이너 시작 스크립트
├── .dockerignore                 # Docker 빌드 제외 파일
├── Makefile                      # 개발 명령어 단축키
├── .pre-commit-config.yaml       # Pre-commit 훅 설정
├── .env.example                  # 환경 변수 템플릿
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI 워크플로우
└── README.md                     # 이 파일
```

## 빠른 시작 (Docker)

Docker를 사용하면 개발 환경을 빠르게 구축할 수 있습니다.

### 필수 요구사항
- Docker Desktop
- Git

### 실행 방법

1. **저장소 클론**
```bash
git clone https://github.com/youngroknroll/spaogame_DRF.git
cd spaogame-api
```

2. **Docker Compose로 실행**
```bash
docker compose up --build
```

3. **서비스 접속**
- API 서버: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

4. **테스트 실행 (컨테이너 내부)**
```bash
docker compose exec web uv run pytest -v
```

5. **종료**
```bash
docker compose down
```

**포함된 서비스:**
- `web`: Django API 서버 (port 8000)
- `db`: PostgreSQL 17 (port 5432)
- `redis`: Redis 7 (port 6379)

**자동 실행 기능:**
- 데이터베이스 연결 대기 (최대 30초)
- 마이그레이션 자동 실행
- 개발 서버 자동 시작

## 설치 및 실행

### 필수 요구사항

- Python 3.13+
- UV (Python 패키지 매니저)
- Git

### 설치 단계

1. **저장소 클론**
```bash
git clone https://github.com/youngroknroll/spaogame_DRF.git
cd spaogame-api
```

2. **UV 설치** (없는 경우)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **환경 변수 설정**
```bash
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env

# SECRET_KEY 생성
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# .env 파일을 열어 생성된 SECRET_KEY를 입력
# DJANGO_SECRET_KEY=<생성된-키-붙여넣기>
# DEBUG=True
# ALLOWED_HOSTS=localhost,127.0.0.1
```

4. **의존성 설치**
```bash
uv sync
```

5. **데이터베이스 마이그레이션**
```bash
uv run python manage.py migrate
# 또는: make migrate
```

6. **슈퍼유저 생성** (관리자 계정)
```bash
uv run python manage.py createsuperuser
```

7. **개발 서버 실행**
```bash
uv run python manage.py runserver
# 또는: make shell
```

서버는 `http://localhost:8000`에서 실행됩니다.

## 데이터베이스 구조

### 핵심 모델

#### Users 앱
- **User**: 사용자 계정 (이메일 기반 인증)
  - 이메일, 이름, 성별, 생년월일 등 확장 필드

#### Products 앱
- **Menu**: 상품 메뉴 (대분류)
- **Category**: 카테고리 (소분류, Menu에 종속)
- **Product**: 상품 정보
  - Menu, Category, 이름, 가격, 설명
  - Menu/Category 무결성 검증 (clean() + DB 제약)
- **Color**: 색상 정보
- **Size**: 사이즈 정보
- **DetailedProduct**: 상품 상세 정보 (Color/Size 조합)
  - unique_together 제약: (product, color, size)
- **Image**: 상품 이미지

#### Orders 앱
- **Cart**: 사용자별 장바구니
- **CartItem**: 장바구니 항목
  - product 또는 detailed_product 중 **정확히 하나만** 설정 (CheckConstraint)
  - UniqueConstraint로 cart + product, cart + detailed_product 중복 방지
- **Wishlist**: 사용자별 위시리스트
- **WishlistItem**: 위시리스트 항목

#### Postings 앱
- **Posting**: 게시글 (상품 후기)
  - 평점, 내용, 이미지 포함
- **Comment**: 댓글

### 데이터 검증

#### CartItem 검증 전략
1. **DB 제약**: CheckConstraint로 product/detailed_product 중 정확히 하나만 설정
2. **모델 검증**: `clean()` 메서드로 유효성 확인
3. **시리얼라이저 검증**: `CartAddSerializer`에서 입력 데이터 검증
4. **UniqueConstraint**: 중복 행 생성 및 race condition 방지

#### Product 검증 전략
1. **모델 검증**: `clean()` 메서드로 category가 menu에 속하는지 확인
2. **시리얼라이저 검증**: `ProductSerializer.validate()`에서 create/update 시 검증

## 주요 기능

### 🔐 인증 및 사용자 관리
- JWT 기반 토큰 인증
- 이메일 기반 회원가입 및 로그인
- 프로필 관리 (성별, 생년월일 등)
- 비밀번호 해싱 (Argon2)

### 🛍️ 상품 관리
- 계층적 카테고리 (Menu → Category → Product)
- 색상/사이즈 조합을 통한 다양한 상품 옵션
- 이미지 관리 (썸네일 지정 가능)
- 상품 검색 및 필터링

### 🛒 주문 및 장바구니
- 장바구니 관리 (상품 추가, 수량 변경, 삭제)
- 위시리스트 관리
- 원자적 데이터 무결성 보장 (DB 제약)

### 💬 게시판 및 리뷰
- 상품 후기 작성 (평점 포함)
- 댓글 기능
- 이미지 첨부

## API 문서

### API 엔드포인트 및 인증

#### 권한 체계
| 권한 타입 | 설명 | 적용 대상 |
|----------|------|----------|
| **공개** | 인증 없이 누구나 접근 가능 | 상품 조회, 후기 조회 등 |
| **인증 필요** | 로그인한 사용자만 접근 가능 | 프로필, 장바구니, 후기 작성 등 |
| **소유자 전용** | 리소스 소유자만 수정/삭제 가능 | 후기 수정/삭제, 댓글 삭제 등 |
| **관리자 전용** | 관리자 권한 필요 | 상품 등록, 카테고리 관리 등 |

#### 인증 및 사용자
- `POST /api/users/signup/` - 회원가입 (공개)
- `POST /api/users/login/` - 로그인, JWT 토큰 발급 (공개)
- `GET /api/users/genders/` - 성별 목록 조회 (공개)
- `GET /api/users/profile/` - 프로필 조회 (인증 필요)
- `PATCH /api/users/profile/` - 프로필 수정 (인증 필요, 본인만)

#### 상품
- `GET /api/products/menus/` - 메뉴 목록 (공개)
- `POST /api/products/menus/` - 메뉴 등록 (관리자 전용)
- `GET /api/products/menus/{menu_id}/categories/` - 특정 메뉴의 카테고리 목록 (공개)
- `POST /api/products/menus/{menu_id}/categories/` - 카테고리 등록 (관리자 전용)
- `GET /api/products/colors/` - 색상 목록 (공개)
- `POST /api/products/colors/` - 색상 등록 (관리자 전용)
- `GET /api/products/sizes/` - 사이즈 목록 (공개)
- `POST /api/products/sizes/` - 사이즈 등록 (관리자 전용)
- `GET /api/products/` - 상품 목록, 필터링/정렬 지원 (공개)
- `POST /api/products/` - 상품 등록 (관리자 전용)
- `GET /api/products/{product_id}/` - 상품 상세 조회 (공개)
- `GET /api/products/{product_id}/images/` - 상품 이미지 목록 (공개)
- `POST /api/products/{product_id}/images/` - 상품 이미지 등록 (관리자 전용)
- `GET /api/products/{product_id}/detailed/` - 상세 상품 목록, 색상/사이즈 조합 (공개)
- `POST /api/products/{product_id}/detailed/` - 상세 상품 등록 (관리자 전용)
- `POST /api/products/{product_id}/postings/` - 상품 후기 작성 (인증 필요)

#### 장바구니
- `GET /api/cart/` - 장바구니 조회 (인증 필요, 본인만)
- `POST /api/cart/` - 장바구니에 상품 추가 (인증 필요)
- `PATCH /api/cart/{item_id}/` - 장바구니 항목 수정 (인증 필요, 본인만)
- `DELETE /api/cart/{item_id}/` - 장바구니 항목 삭제 (인증 필요, 본인만)

#### 위시리스트
- `GET /api/wishlist/` - 위시리스트 조회 (인증 필요, 본인만)
- `POST /api/wishlist/` - 위시리스트에 상품 추가 (인증 필요)
- `DELETE /api/wishlist/{item_id}/` - 위시리스트 항목 삭제 (인증 필요, 본인만)

#### 후기 (Postings)
- `GET /api/postings/` - 후기 목록 조회 (공개)
- `GET /api/postings/{posting_id}/` - 후기 상세 조회 (공개)
- `POST /api/products/{product_id}/postings/` - 후기 작성 (인증 필요)
- `PATCH /api/postings/{posting_id}/` - 후기 수정 (소유자 전용)
- `DELETE /api/postings/{posting_id}/` - 후기 삭제 (소유자 전용)

#### 댓글 (Comments)
- `POST /api/postings/{posting_id}/comments/` - 댓글 작성 (인증 필요)
- `DELETE /api/postings/{posting_id}/comments/{comment_id}/` - 댓글 삭제 (소유자 전용)

### 자동 API 문서
- **Swagger UI**: `/api/schema/swagger-ui/`
- **ReDoc**: `/api/schema/redoc/`
- **OpenAPI 스키마**: `/api/schema/`

### API 사용 예시

#### 회원가입
```bash
curl -X POST http://localhost:8000/api/users/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "name": "홍길동",
    "gender": "M"
  }'
```

**응답 예시:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "홍길동",
  "gender": "M",
  "date_joined": "2024-01-15T10:30:00Z"
}
```

#### 로그인 (JWT 토큰 발급)
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

**응답 예시:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 프로필 조회 (인증 필요)
```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer <access_token>"
```

**응답 예시:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "홍길동",
  "username": null,
  "mobile_number": null,
  "address1": null,
  "address2": null,
  "birthday": null,
  "gender": "M",
  "date_joined": "2024-01-15T10:30:00Z"
}
```

#### 상품 목록 조회 (필터링)
```bash
# 특정 메뉴와 카테고리로 필터링
curl -X GET "http://localhost:8000/api/products/?menu=1&category=2&ordering=-created_at"

# 가격 범위로 필터링
curl -X GET "http://localhost:8000/api/products/?min_price=10000&max_price=50000"
```

#### 장바구니에 상품 추가
```bash
curl -X POST http://localhost:8000/api/cart/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

#### 후기 작성
```bash
curl -X POST http://localhost:8000/api/products/1/postings/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "정말 좋은 상품입니다!",
    "content": "품질이 우수하고 배송도 빨랐어요.",
    "rating": 5
  }'
```

#### 후기 수정 (소유자만)
```bash
curl -X PATCH http://localhost:8000/api/postings/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "수정된 제목",
    "rating": 4
  }'
```

## 개발 가이드

### Makefile 명령어

프로젝트는 자주 사용하는 명령어를 단축키로 제공합니다.

```bash
make help          # 사용 가능한 명령어 목록
make install       # 의존성 설치
make test          # 테스트 실행
make lint          # 린팅 검사
make format        # 코드 포맷
make clean         # 캐시 파일 정리
make docker-up     # Docker 서비스 시작
make docker-down   # Docker 서비스 종료
make migrate       # 마이그레이션 실행
make shell         # Django shell 시작
```

### 코드 품질 관리

#### Ruff (린터 & 포매터)

```bash
# 코드 린팅
make lint
# 또는: uv run ruff check .

# 코드 포맷
make format
# 또는: uv run ruff format .

# 자동 수정
uv run ruff check --fix .
```

**Ruff 설정:**
- Line length: 100
- Target: Python 3.13
- Rules: pycodestyle, pyflakes, isort, flake8-bugbear, comprehensions, pyupgrade

#### Pre-commit 훅

Git commit 전에 자동으로 린팅 및 포맷을 실행합니다.

```bash
# Pre-commit 훅 설치
uv run pre-commit install

# 모든 파일에 대해 수동 실행
uv run pre-commit run --all-files
```

**Pre-commit 검사 항목:**
- Trailing whitespace 제거
- EOF 수정
- YAML/JSON/TOML 검증
- Private key 감지
- Ruff 린팅 및 포맷

### 테스트 실행

**테스트 통계:**
- 총 테스트: 74개
- 테스트 프레임워크: pytest + pytest-django
- 테스트 커버리지: apps/ 디렉토리 전체
- 테스트 명명: 한글 함수명 (Given-When-Then 패턴)

```bash
# 모든 테스트 실행
make test
# 또는: uv run pytest

# 상세 출력과 함께 실행
uv run pytest -v

# 특정 앱의 테스트만 실행
uv run pytest apps/users/tests/

# 특정 테스트 파일 실행
uv run pytest apps/postings/tests/test_postings_crud.py

# 커버리지 리포트 생성 (자동)
uv run pytest  # coverage.xml과 터미널 리포트 자동 생성

# HTML 커버리지 리포트
uv run pytest --cov=apps --cov-report=html
open htmlcov/index.html
```

**테스트 구성:**
- `apps/users/tests/`: 회원가입, 로그인, 프로필 테스트
- `apps/products/tests/`: 상품, 카테고리, 색상/사이즈 테스트
- `apps/orders/tests/`: 장바구니, 위시리스트 테스트
- `apps/postings/tests/`: 후기, 댓글 테스트

**Docker에서 테스트 실행:**
```bash
docker compose exec web uv run pytest -v
```

### 마이그레이션 관리

```bash
# 마이그레이션 파일 생성
uv run python manage.py makemigrations apps

# 마이그레이션 상태 확인
uv run python manage.py showmigrations

# 특정 마이그레이션으로 롤백
uv run python manage.py migrate apps 0001
```

### 관리자 페이지
- URL: `http://localhost:8000/admin/`
- 슈퍼유저 계정으로 로그인
- 모든 모델 관리 가능

### 개발 방법론 (TDD)

이 프로젝트는 **테스트 주도 개발(TDD)** 방법론을 따릅니다.

#### TDD 사이클: Red → Green → Refactor

**1. Red (실패하는 테스트 작성)**
```bash
# 테스트 파일 작성 (예: test_profile.py)
def test_인증_로그인한_사용자는_자신의_프로필을_조회할_수_있다(user_client, regular_user):
    response = user_client.get(API_USERS_PROFILE)
    assert response.status_code == status.HTTP_200_OK
```

**2. Green (최소한의 코드로 테스트 통과)**
```python
# views.py에 최소한의 구현
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
```

**3. Refactor (코드 개선)**
- 중복 코드 제거
- 가독성 향상
- 성능 최적화
- 테스트는 계속 통과해야 함

#### TDD 실천 규칙

1. **테스트 먼저, 구현 나중**
   - 기능 구현 전에 항상 테스트 작성
   - 테스트가 실패하는 것을 확인한 후 구현

2. **한 번에 하나의 테스트**
   - 작은 단위로 테스트 작성
   - 각 테스트는 하나의 행동/시나리오만 검증

3. **명확한 테스트 이름**
   - Given-When-Then 패턴 사용
   - 한글 함수명으로 의도 명확히 표현
   - 예: `test_인증_로그인한_사용자는_자신의_프로필을_조회할_수_있다`

4. **테스트 독립성**
   - 각 테스트는 독립적으로 실행 가능
   - fixtures 사용으로 테스트 데이터 격리

#### 테스트 작성 예시

```python
@pytest.mark.django_db
def test_권한_후기_작성자가_아닌_사용자는_후기를_수정할_수_없다(user_client, another_user_posting):
    """
    Given: 다른 사용자가 작성한 후기가 있을 때
    When: 로그인한 사용자가 다른 사용자의 후기를 수정하려고 하면
    Then: 권한 오류가 발생한다
    """
    url = API_POSTING_DETAIL.format(posting_id=another_user_posting.id)
    update_data = {"title": "수정 시도", "rating": 1}

    response = user_client.patch(url, update_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN
```

### 코드 스타일 및 아키텍처

**코드 스타일:**
- PEP 8 준수
- 한글 테스트 함수명 (Given-When-Then)
- Docstring으로 API 동작 문서화

**아키텍처 원칙:**
- **CBV (Class-Based Views)** 사용
- 각 앱에서 독립적인 테스트 작성
- 시리얼라이저에서 데이터 검증
- 모델의 `clean()` 메서드로 비즈니스 로직 검증
- DB 제약으로 데이터 무결성 보장
- 권한 클래스로 접근 제어 분리

### 환경 변수 설정

| 환경 변수 | 기본값 | 설명 | 예시 |
|---------|------|------|------|
| `DJANGO_SECRET_KEY` | **필수** | Django 시크릿 키 | `your-secret-key-here` |
| `DEBUG` | `False` | 디버그 모드 (개발: True, 운영: False) | `True` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | 허용된 호스트 (쉼표로 구분) | `example.com,www.example.com` |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | 데이터베이스 연결 URL | `postgresql://user:pass@db:5432/spaogame` |
| `REDIS_URL` | - | Redis 연결 URL (선택) | `redis://redis:6379/0` |

**SECRET_KEY 생성 방법:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**DATABASE_URL 형식:**
```bash
# SQLite (개발)
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL (운영)
DATABASE_URL=postgresql://username:password@host:port/database

# Docker Compose
DATABASE_URL=postgresql://spaogame:spaogame_password@db:5432/spaogame
```

**`.env` 파일 예시:**
```bash
DJANGO_SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## CI/CD

### GitHub Actions

프로젝트는 GitHub Actions를 통해 자동화된 테스트 및 코드 품질 검사를 수행합니다.

**워크플로우:** `.github/workflows/ci.yml`

**실행 조건:**
- `main` 브랜치에 push
- `main` 브랜치로의 Pull Request

**검사 항목:**
1. **Ruff 린팅**: 코드 스타일 및 품질 검사
2. **Ruff 포맷 검사**: 코드 포맷 일관성 확인
3. **테스트 실행**: PostgreSQL 환경에서 74개 테스트 실행
4. **커버리지 리포트**: Codecov 업로드 (선택)

**테스트 환경:**
- Python 3.13
- PostgreSQL 17
- UV 패키지 매니저

**로컬에서 CI 시뮬레이션:**
```bash
# 린팅 검사
make lint

# 포맷 검사
uv run ruff format --check .

# 테스트 실행
make test
```

**Badge 상태 확인:**
- CI Status: ![CI](https://github.com/youngroknroll/spaogame_DRF/workflows/CI/badge.svg)

## 보안 고려사항

### 구현된 보안 조치
- ✅ 환경 변수 기반 설정 (SECRET_KEY, DEBUG, DATABASE_URL)
- ✅ SECRET_KEY 필수값 검증 (누락 시 명확한 에러)
- ✅ DEBUG 기본값 False (운영 환경 안전)
- ✅ Argon2 기반 비밀번호 해싱
- ✅ JWT 토큰 기반 인증
- ✅ 데이터베이스 제약을 통한 무결성 보장
- ✅ 입력 데이터 검증 (시리얼라이저, 모델)
- ✅ Pre-commit 훅으로 private key 감지

### 권장 프로덕션 설정
- ✅ `DEBUG = False` 기본값 적용
- ✅ `ALLOWED_HOSTS`에 실제 도메인 지정
- ✅ 환경 변수로 SECRET_KEY 관리
- ✅ PostgreSQL 사용 (Docker Compose 지원)
- ⚠️ HTTPS 강제 (배포 환경에서 설정 필요)
- ⚠️ CSRF 보호 활성화
- ⚠️ CORS 정책 설정
- ✅ `.env` 파일 VCS 제외 (.gitignore)

## 최근 업데이트

### v0.3.0 - 배포 인프라 구축 (2026-02-10)

**Phase 1: 환경 설정 개선**
- ✅ `.env.example` 템플릿 제공
- ✅ SECRET_KEY 필수값 검증 (누락 시 명확한 에러 메시지)
- ✅ DEBUG 기본값 False로 변경 (운영 환경 보안 강화)
- ✅ DATABASE_URL 환경변수 지원 (dj-database-url)
- ✅ PostgreSQL 지원 추가 (psycopg[binary] 3.3.2)
- ✅ Gunicorn WSGI 서버 추가

**Phase 2: Docker 환경 구축**
- ✅ Multi-stage Dockerfile (Python 3.13, UV)
- ✅ docker-compose.yml (Django + PostgreSQL 17 + Redis 7)
- ✅ 마이그레이션 자동화 (docker-entrypoint.sh)
- ✅ Health check 설정
- ✅ Volume 마운트로 개발 편의성 향상
- ✅ Docker 환경에서 74/74 테스트 통과

**Phase 3: CI/CD**
- ✅ GitHub Actions 워크플로우 (.github/workflows/ci.yml)
- ✅ PostgreSQL 17 서비스 컨테이너
- ✅ Ruff 린팅 및 포맷 검사 자동화
- ✅ pytest 자동 실행 및 커버리지 리포트
- ✅ main 브랜치 push/PR 시 자동 실행

**Phase 4: 린팅/포맷팅**
- ✅ Ruff 0.15.0 통합 (린터 + 포매터)
- ✅ pyproject.toml 설정 (line-length 100, Python 3.13)
- ✅ Pre-commit 훅 설정 (.pre-commit-config.yaml)
- ✅ Makefile 추가 (자주 사용하는 명령어 단축)
- ✅ 전체 코드베이스 Ruff 포맷 적용 (63개 파일)
- ✅ pytest-cov 통합 (coverage.xml 자동 생성)

**개발 도구:**
- `make test` - 테스트 실행
- `make lint` - 린팅 검사
- `make format` - 코드 포맷
- `make docker-up` - Docker 서비스 시작
- `make docker-down` - Docker 서비스 종료

**검증:**
- ✅ 로컬 테스트: 74/74 통과
- ✅ Docker 테스트: 74/74 통과
- ✅ Ruff 린트: All checks passed
- ✅ Pre-commit 훅: 설치 및 동작 확인

### v0.2.0 - 기능 확장 (2026-01)

- **프로필 관리 API**: 사용자 프로필 조회 및 수정 기능
- **후기 CRUD API**: 상품 후기 목록 조회 및 관리
- **테스트 확장**: 총 74개 테스트 (프로필, 후기 CRUD 포함)
- **README 개선**: API 사용 예시, TDD 방법론 문서화

### v0.1.0 - 초기 릴리스 (2025-12)

- **CartItem 검증 강화**: DB 제약으로 데이터 무결성 보장
- **Product 무결성**: category-menu 관계 검증
- **환경 변수화**: DEBUG, ALLOWED_HOSTS 환경 변수 관리
- **CBV 통일**: Class-Based Views 스타일
- **위시리스트 기능**: 사용자별 위시리스트 관리

## 라이센스

MIT License
