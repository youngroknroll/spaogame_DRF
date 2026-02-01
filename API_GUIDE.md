# SPAOGAME API 완전 가이드

## 📦 Postman Collection Import

### 파일
[SPAOGAME_API_Complete.postman_collection.json](SPAOGAME_API_Complete.postman_collection.json)

### Import 방법
1. Postman 실행
2. **"Import"** 클릭
3. 파일 드래그 앤 드롭
4. 우측 상단에서 **"SPAOGAME Development"** 환경 선택

---

## 🔐 권한 아이콘

- 🌍 **AllowAny**: 인증 불필요 (누구나 접근 가능)
- 🔒 **IsAuthenticated**: JWT 토큰 필요
- 👤 **IsOwner**: 본인 리소스만 수정/삭제
- 👑 **IsAdmin**: 관리자 권한 (is_staff=True)

---

## 🚀 빠른 시작

### 1. 서버 실행
```bash
uv run python manage.py runserver
```

### 2. 회원가입 & 로그인
```
1. "1. Auth & Users" → "회원가입" 실행
2. "로그인" 실행 → JWT 토큰 자동 저장
```

### 3. API 테스트
이제 모든 엔드포인트를 테스트할 수 있습니다!

---

## 📚 API 구조

### 1. Auth & Users
| 엔드포인트 | 메서드 | 권한 | 설명 |
|---|---|---|---|
| `/api/users/signup/` | POST | 🌍 | 회원가입 |
| `/api/users/login/` | POST | 🌍 | 로그인 (JWT 발급) |
| `/api/users/genders/` | GET | 🌍 | 성별 선택지 |
| `/api/users/profile/` | GET | 🔒 | 내 프로필 조회 |
| `/api/users/profile/` | PATCH | 🔒 | 내 프로필 수정 |

### 2. Products - Menu & Category
| 엔드포인트 | 메서드 | 권한 | 설명 |
|---|---|---|---|
| `/api/products/menus/` | GET | 🌍 | 메뉴 목록 |
| `/api/products/menus/` | POST | 👑 | 메뉴 등록 |
| `/api/products/menus/:id/categories/` | GET | 🌍 | 카테고리 목록 |
| `/api/products/menus/:id/categories/` | POST | 👑 | 카테고리 등록 |

### 3. Products - Options
| 엔드포인트 | 메서드 | 권한 | 설명 |
|---|---|---|---|
| `/api/products/colors/` | GET | 🌍 | 색상 목록 |
| `/api/products/colors/` | POST | 👑 | 색상 등록 |
| `/api/products/sizes/` | GET | 🌍 | 사이즈 목록 |
| `/api/products/sizes/` | POST | 👑 | 사이즈 등록 |

### 4. Products - Items
| 엔드포인트 | 메서드 | 권한 | 설명 |
|---|---|---|---|
| `/api/products/` | GET | 🌍 | 상품 목록 |
| `/api/products/` | POST | 👑 | 상품 등록 |
| `/api/products/:id/` | GET | 🌍 | 상품 상세 (평점, 후기 포함) |
| `/api/products/:id/images/` | GET | 🌍 | 상품 이미지 목록 |
| `/api/products/:id/images/` | POST | 👑 | 이미지 등록 |
| `/api/products/:id/detailed/` | GET | 🌍 | 재고 정보 (색상/사이즈별) |
| `/api/products/:id/detailed/` | POST | 👑 | 재고 등록 |

**필터링 & 정렬:**
- `?menu=1` - 메뉴별 필터
- `?category=1` - 카테고리별 필터
- `?ordering=price` - 가격 오름차순
- `?ordering=-price` - 가격 내림차순

### 5. Postings (Reviews)
| 엔드포인트 | 메서드 | 권한 | 설명 |
|---|---|---|---|
| `/api/postings/` | GET | 🌍 | 전체 후기 목록 |
| `/api/products/:id/postings/` | POST | 🔒 | 후기 작성 |
| `/api/postings/:id/` | GET | 🌍 | 후기 상세 (댓글 포함) |
| `/api/postings/:id/` | PATCH | 👤 | 후기 수정 |
| `/api/postings/:id/` | DELETE | 👤 | 후기 삭제 |

### 6. Comments
| 엔드포인트 | 메서드 | 권한 | 설명 |
|---|---|---|---|
| `/api/postings/:id/comments/` | POST | 🔒 | 댓글 작성 |
| `/api/postings/:id/comments/:id/` | DELETE | 👤 | 댓글 삭제 |

### 7. Cart (장바구니)
| 엔드포인트 | 메서드 | 권한 | 설명 |
|---|---|---|---|
| `/api/cart/` | GET | 🔒 | 장바구니 조회 |
| `/api/cart/` | POST | 🔒 | 상품 추가 |
| `/api/cart/:id/` | PATCH | 🔒 | 수량 변경 |
| `/api/cart/:id/` | DELETE | 🔒 | 항목 삭제 |

**상품 추가 방식:**
```json
// 기본 상품 추가
{
  "product_id": 1,
  "quantity": 2
}

// 상세 상품 추가 (색상/사이즈 지정)
{
  "detailed_product_id": 1,
  "quantity": 1
}
```

### 8. Wishlist (위시리스트)
| 엔드포인트 | 메서드 | 권한 | 설명 |
|---|---|---|---|
| `/api/wishlist/` | GET | 🔒 | 위시리스트 조회 |
| `/api/wishlist/` | POST | 🔒 | 상품 추가 |
| `/api/wishlist/:id/` | DELETE | 🔒 | 항목 삭제 |

---

## 🎯 추천 테스트 시나리오

### 시나리오 1: 상품 구매 플로우
```
1. 메뉴 목록 조회
2. 카테고리 목록 조회
3. 상품 목록 조회 (필터링)
4. 상품 상세 조회
5. 상세 상품 조회 (재고 확인)
6. 장바구니에 추가
7. 장바구니 조회
```

### 시나리오 2: 후기 작성 플로우
```
1. 상품 상세 조회 (현재 평점 확인)
2. 후기 작성
3. 상품 상세 재조회 (평점 업데이트 확인)
4. 후기 목록 조회
5. 댓글 작성
```

### 시나리오 3: 관리자 상품 등록
```
1. 메뉴 등록
2. 카테고리 등록
3. 색상/사이즈 등록
4. 상품 등록
5. 이미지 등록
6. 상세 상품 등록 (재고)
```

---

## 🔧 관리자 권한 설정

### Django Admin에서 설정
```bash
uv run python manage.py createsuperuser
```

### Django Shell에서 설정
```bash
uv run python manage.py shell
```

```python
from apps.users.models import User

user = User.objects.get(email='user@example.com')
user.is_staff = True
user.save()
```

---

## 📊 응답 예시

### 회원가입 성공
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "홍길동",
  "message": "회원가입이 완료되었습니다."
}
```

### 로그인 성공
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 상품 상세 조회
```json
{
  "id": 1,
  "name": "나이키 축구화",
  "price": 180000,
  "description": "최고급 축구화",
  "menu": {...},
  "category": {...},
  "thumbnail_url": "https://...",
  "posting_count": 15,
  "average_rating": 4.5,
  "available_colors": [...],
  "available_sizes": [...],
  "images": [...]
}
```

### 장바구니 조회
```json
{
  "id": 1,
  "items": [
    {
      "id": 1,
      "product": {...},
      "detailed_product": {...},
      "quantity": 2,
      "subtotal": 360000
    }
  ],
  "total_price": 360000,
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## ⚠️ 주의사항

### JWT 토큰 만료
- Access 토큰 유효기간: 설정에 따라 다름
- 만료 시 다시 로그인 필요

### 권한 에러
```json
{
  "detail": "Authentication credentials were not provided."
}
```
→ Authorization 헤더 확인

### 본인 리소스 아님
```json
{
  "detail": "이 작업을 수행할 권한이 없습니다."
}
```
→ 다른 사용자의 후기/댓글은 수정/삭제 불가

---

## 🐛 문제 해결

### 401 Unauthorized
- 로그인 요청을 다시 실행
- Environment에서 `token` 변수 확인

### 404 Not Found
- URL 경로 확인
- 리소스 ID가 존재하는지 확인

### 400 Bad Request
- Request Body 형식 확인
- 필수 필드 누락 확인

---

## 📖 추가 리소스

- **캐싱 테스트 Collection**: [SPAOGAME_API_Cache_Tests.postman_collection.json](SPAOGAME_API_Cache_Tests.postman_collection.json)
- **캐싱 구현 상세**: [config/settings.py](config/settings.py#L169-L188)
- **API 스키마**: `http://localhost:8000/api/schema/swagger/` (drf-spectacular)
