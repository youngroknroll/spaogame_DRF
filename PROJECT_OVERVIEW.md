# SPAOGAME Backend 문서

이 문서는 현재 백엔드 코드 기준으로 구조와 API 동작을 요약합니다. 실제 동작은 데이터 및 설정에 따라 달라질 수 있습니다.

## 개요
- 프레임워크: Django 3.2
- DB: MySQL
- 인증: JWT (헤더 `Authorization`)
- 주요 앱: `users`, `products`, `postings`, `orders`, `core`
- URL 규칙: `APPEND_SLASH = False` 이므로 기본적으로 끝 슬래시 없음

## 요구사항
- Python 3.x
- Django 3.2
- MySQL (pymysql 사용)
- 환경 변수/시크릿: `my_settings.py` 또는 `spao/settings.py` 기반
- 필수 의존성 목록: `requirements.txt`

## 디렉토리 구조 (요약)
- `spao/` Django 프로젝트 설정 및 루트 URL
- `users/` 회원가입/로그인, 사용자 및 성별 모델
- `products/` 메뉴/카테고리/상품/상세 상품 관련
- `postings/` 후기/댓글 관련
- `orders/` 장바구니 관련
- `core/` 공통 타임스탬프 모델

## 인증/인가
- 로그인 시 JWT 발급 (`/users/signin`)
- 인증 필요한 API는 `Authorization` 헤더에 토큰 전달
- 데코레이터: `users.decorators.login_decorator`
- 역할 기반 권한은 구현되어 있지 않음 (관리자/일반 사용자 구분 없음)

## 권한 매트릭스
- 공개 접근: `POST /users/signup`, `POST /users/signin`, 모든 `GET /products/*`, `GET /products/main`
- 인증 필요: `POST /postings`, `POST /postings/comments`, `DELETE /postings/comments/<comment_id>`, `POST/GET/PATCH/DELETE /orders/cart`

## 모델 요약
### `core`
- `TimeStampedModel`: `created_at`, `updated_at`, `deleted_at` 공통 필드

### `users`
- `Gender(name)`
- `User(username, password, name, email, mobile_number, address1, address2, birthday, gender)`

### `products`
- `Menu(name)`
- `Category(menu, name)`
- `Product(menu, category, name, price, description, quantity, thumbnail_image_url)`
- `Color(name)`
- `Size(name)`
- `Image(product, posting, urls)`
- `DetailedProduct(color, size, product)`

### `postings`
- `Posting(user, product, title, content, rating)`
- `Comment(user, posting, content)`

### `orders`
- `Wishlist(user, product)`
- `Basket(user, product(detailed), quantity)`

## API 목록
기본 Prefix는 `spao/urls.py` 기준으로 `/users`, `/products`, `/postings`, `/orders` 입니다.

### Users
#### `POST /users/signup`
- Body
  - `username`, `password`, `name`, `email`, `mobile_number`
  - `address1`, `address2`(optional), `birthday`, `gender`
- 동작: 이메일/비밀번호 정규식 검사, 중복 검사 후 회원 생성

#### `POST /users/signin`
- Body: `email`, `password`
- 응답: `{"TOKEN": "<jwt>"}`

### Products
#### `POST /products/menus`
- Body: `name`

#### `GET /products/menus`
- 응답: 메뉴 리스트

#### `POST /products/categories`
- Body: `menu_id`, `name`

#### `GET /products/menus/<menu_name>`
- 응답: 해당 메뉴의 카테고리 목록

#### `POST /products`
- Body: `menu_id`, `category_id`, `name`, `price`, `description`, `quantity`, `thumb_url`, `img_urls`
- `img_urls`는 배열

#### `GET /products/<menu_name>/<category_name>`
- Query: `offset`(default 0), `limit`(default 15, 최대 20), `order_id`(0=최신, 1=높은가격, 2=낮은가격, 3=이름)
- 응답: 상품 리스트 (색상/리뷰 수 포함)

#### `GET /products/<id>`
- 응답: 상세 상품 + 리뷰/댓글 정보 포함

#### `GET /products/main`
- 응답: 전체 상품 썸네일 목록

### Postings
#### `POST /postings`
- 인증 필요
- Body: `review_content`, `title`, `product_id`

#### `POST /postings/comments`
- 인증 필요
- Body: `comment_content`, `posting_id`

#### `DELETE /postings/comments/<comment_id>`
- 인증 필요

### Orders (Cart)
#### `POST /orders/cart`
- 인증 필요
- Body: `product_id`, `color_name`, `size_name`, `quantity`

#### `GET /orders/cart`
- 인증 필요
- 응답: 장바구니 리스트 (상품/색상/사이즈/수량)

#### `PATCH /orders/cart`
- 인증 필요
- Body: `quantity`, `detailed_product_id`

#### `DELETE /orders/cart`
- 인증 필요
- Body: `basket_id`

## 에러 응답 규격 (현 구현 기준)
표준 에러 스키마가 통일되어 있지 않습니다. 현재는 주로 아래 형태를 사용합니다.
- 공통 형태: `{"MESSAGE": "ERROR_CODE"}` 또는 `{"message": "ERROR_CODE"}`
- 상태코드는 엔드포인트별로 상이하며, 일부는 동일 오류라도 다른 코드 사용

### 공통적으로 관찰되는 에러 코드 예시
- 인증: `DECODE_ERROR`, `USER_NOTEXIST`
- 회원가입/로그인: `EMAIL_VALIDATION_ERROR`, `PASSWORD_VALIDATION_ERROR`, `DUPLICATION_ERROR`, `USER_DOES_NOT_EXIST`, `INVALID_USER`, `KEY_ERROR`
- 장바구니: `DOES_NOT_EXIST`, `ALREADY_EXIST`, `NOTING_IN_CART`
- 후기/댓글: `JSON_DECODE_ERROR`, `KEYERROR`, `POSTING-DOES-NOT-EXIST`

### 주의사항
- 일부 뷰는 `message` 키와 `MESSAGE` 키를 혼용
- 일부 에러는 메시지 형식이 다름 (`KEY-ERROR`, `KEYERROR`, `KEY_ERROR` 등)

## 참고
- DB 설정 및 시크릿 키는 `spao/settings.py`, `my_settings.py`에 정의
- 실제 환경 구성은 별도 설정으로 분리하는 것을 권장
