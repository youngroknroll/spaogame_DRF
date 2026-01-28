# Spaogame API

Django REST Framework 기반의 전자상거래 플랫폼 API 서버

## 📋 목차

- [개요](#개요)
- [기술 스택](#기술-스택)
- [프로젝트 구조](#프로젝트-구조)
- [설치 및 실행](#설치-및-실행)
- [데이터베이스 구조](#데이터베이스-구조)
- [주요 기능](#주요-기능)
- [API 문서](#api-문서)
- [개발 가이드](#개발-가이드)

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
| **데이터베이스** | SQLite (개발), PostgreSQL 권장 (프로덕션) |
| **비밀번호 해싱** | Argon2 |
| **환경 설정** | python-dotenv 1.2.1 |
| **테스팅** | pytest 9.0.2, pytest-django 4.11.1 |
| **Python** | 3.13+ |

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
├── manage.py                     # Django 관리 스크립트
├── main.py                       # 진입점
└── README.md                     # 이 파일
```

## 설치 및 실행

### 필수 요구사항

- Python 3.13+
- uv (Python 패키지 매니저)
- Git

### 설치 단계

1. **저장소 클론**
```bash
git clone https://github.com/your-username/spaogame-api.git
cd spaogame-api
```

2. **환경 변수 설정**
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 수정
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

3. **의존성 설치**
```bash
uv sync
```

4. **데이터베이스 마이그레이션**
```bash
uv run python manage.py migrate
```

5. **슈퍼유저 생성** (관리자 계정)
```bash
uv run python manage.py createsuperuser
```

6. **개발 서버 실행**
```bash
uv run python manage.py runserver
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

### 테스트 실행

**테스트 통계:**
- 총 테스트: 69개
- 테스트 프레임워크: pytest + pytest-django
- 테스트 커버리지: 주요 기능 100%
- 테스트 명명: 한글 함수명 (Given-When-Then 패턴)

```bash
# 모든 테스트 실행
uv run pytest

# 특정 앱의 테스트만 실행
uv run pytest apps/users/tests/

# 특정 테스트 파일 실행
uv run pytest apps/postings/tests/test_postings_crud.py

# 상세 출력과 함께 실행
uv run pytest -v

# 커버리지 리포트 생성
uv run pytest --cov=apps --cov-report=html
```

**테스트 구성:**
- `apps/users/tests/`: 회원가입, 로그인, 프로필 테스트 (12개)
- `apps/products/tests/`: 상품, 카테고리, 색상/사이즈 테스트 (21개)
- `apps/orders/tests/`: 장바구니, 위시리스트 테스트 (19개)
- `apps/postings/tests/`: 후기, 댓글 테스트 (17개)

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

### 주요 설정 (환경 변수)

| 환경 변수 | 기본값 | 설명 |
|---------|------|------|
| `DEBUG` | `True` | 디버그 모드 (프로덕션에서는 `False`로 설정) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | 허용된 호스트 (쉼표로 구분) |
| `DJANGO_SECRET_KEY` | 필수 | Django 시크릿 키 |
| `DATABASE_URL` | SQLite | 데이터베이스 연결 URL |

## 보안 고려사항

### 구현된 보안 조치
- ✅ 환경 변수 기반 설정 (DEBUG, ALLOWED_HOSTS)
- ✅ Argon2 기반 비밀번호 해싱
- ✅ JWT 토큰 기반 인증
- ✅ 데이터베이스 제약을 통한 무결성 보장
- ✅ 입력 데이터 검증 (시리얼라이저, 모델)

### 권장 프로덕션 설정
- `DEBUG = False` 설정
- `ALLOWED_HOSTS`에 실제 도메인 지정
- HTTPS 강제
- CSRF 보호 활성화
- CORS 정책 설정
- 데이터베이스를 PostgreSQL로 변경
- 환경 변수 파일 `.env`를 VCS에서 제외

## 최근 업데이트 (v0.2.0)

### 새로운 기능 (v0.2.0)
- **프로필 관리 API**: 사용자 프로필 조회 및 수정 기능 추가
  - `GET /api/users/profile/` - 로그인한 사용자 프로필 조회
  - `PATCH /api/users/profile/` - 프로필 수정 (이메일, 가입일 read-only)
  - 전화번호, 성별 등 필드 검증 로직 포함
- **후기 CRUD API**: 상품 후기 목록 조회 및 관리 기능 추가
  - `GET /api/postings/` - 후기 목록 조회 (공개)
  - `GET /api/postings/{posting_id}/` - 후기 상세 조회 (공개)
  - `PATCH /api/postings/{posting_id}/` - 후기 수정 (소유자만)
  - `DELETE /api/postings/{posting_id}/` - 후기 삭제 (소유자만)
  - `IsPostingOwner` 권한 클래스로 소유자 검증
- **테스트 확장**: 총 69개 테스트로 확장 (프로필 5개, 후기 CRUD 7개 추가)
- **README 개선**: API 사용 예시, TDD 방법론, 권한 체계 문서화

### 이전 버그 수정 및 개선사항 (v0.1.0)
- **CartItem 검증 강화**: product/detailed_product 중 정확히 하나만 설정되도록 DB 제약 추가
- **중복 행 방지**: CartItem에 조건부 UniqueConstraint 추가로 race condition 방지
- **Product 무결성**: category가 menu에 속하는지 모델 검증 및 DB 제약 추가
- **환경 변수화**: DEBUG와 ALLOWED_HOSTS를 환경 변수로 관리하여 배포 시 보안 강화
- **CBV 통일**: 전체 앱을 Class-Based Views 스타일로 통일
- **위시리스트 기능**: 사용자별 위시리스트 관리 기능 추가

## 라이센스

MIT License