# plan.md

## 0. 목적
- SPAOGAME 백엔드를 DRF로 처음부터 재빌드한다.
- test_list.md를 단일 진실 공급원(Test List)으로 삼는다.
- Kent Beck의 TDD 방식(테스트 목록 → 하나씩 Red/Green/Refactor)을 따른다.
- 테스트는 개발자뿐 아니라 비개발자와의 커뮤니케이션 도구로도 사용한다.

---

## 1. 범위
- MVP 범위는 test_list.md에 정의된 테스트 목록으로 한정한다.
- test_list.md에 없는 기능은 구현하지 않는다.
- 추가 요구사항은 반드시 test_list.md에 테스트 항목으로 먼저 추가한다.

### 문서 대비 누락 항목 관리
- 기존 pure Django 문서(`PROJECT_OVERVIEW.md`)와의 차이를 `test_list.md`의 "문서 대비 추가 누락 항목(Backlog)"에 기록한다.
- Backlog 항목은 우선순위/범위 확정 시 MVP 범위에 편입한다.

---

## 2. 기술 및 환경 결정
- Python: 3.13
- Framework: Django + Django REST Framework
- 패키지 관리 및 실행: uv
- 인증 방식: JWT (SimpleJWT 사용)
- 비밀번호 해시: Argon2
- API 문서화: drf-spectacular
- 데이터베이스: 개발은 sqlite, 운영은 postgres 전환 가능 구조

---

## 3. 프로젝트 구조 규칙
- 모든 도메인 앱은 apps/ 하위에 둔다.
  - 예: apps/users, apps/products, apps/orders, apps/postings
- 역할 분리 원칙
  - View: HTTP 요청/응답 처리, 얇게 유지
  - Serializer: 요청/응답 계약 및 입력 검증
  - Service: 비즈니스 규칙 및 트랜잭션 경계
  - Selector: 조회 전용 로직 및 성능 최적화
- 테스트 위치
  - API 통합 테스트: tests/api/...
  - 도메인 규칙 테스트(선택): apps/<domain>/tests/...

---

## 4. 테스트 작성 규칙 (중요)
테스트는 코드이자 문서이며, 커뮤니케이션 수단이다.
테스트는 “의도(행위)”만 말하고, 기술(HTTP/URL/인증 헤더/ORM) 노출은 최소화한다.
중복은 fixture/헬퍼로 흡수하고, 변경 파급을 한 곳에 가둔다.

### 4.0 기술 노출 최소화 원칙
테스트 코드에서 기술적 세부사항을 숨기고 행위에 집중한다.

**Fixture 활용:**
- 테스트 데이터는 fixture로 추출 (`conftest.py`)
- 예: `valid_signup_payload`, `registered_user` 등
- 변경 시 한 곳만 수정하면 모든 테스트에 반영

**헬퍼 함수 활용:**
- HTTP 요청은 헬퍼 함수로 추상화
- 예: `signup(payload)`, `login(credentials)` 등
- URL, HTTP 메서드는 헬퍼 내부에 숨김

**테스트 본문:**
```python
# ❌ 기술 노출
response = api_client.post("/api/users/signup/", {"email": "...", ...})

# ✅ 행위 중심
response = signup(valid_signup_payload)
```

db 접근이 필요한 테스트에만 django_db를 선언한다.
가능하면 fixture 레벨에서만 선언한다.

테스트는 DB를 직접 알 수 없다.
fixture가 db 의존성을 캡슐화한다.

### 4.1 한글 테스트명 원칙
- 테스트 함수명은 한글을 사용한다.
- 사용자 관점의 “행위와 결과”를 한 문장으로 표현한다.
- 구현 세부사항(모델, 시리얼라이저, DB 등)은 테스트명에 드러내지 않는다.

예:
- 회원가입을_하면_사용자가_생성된다
- 로그인에_성공하면_토큰을_발급받는다
- 존재하지_않는_상품은_조회할_수_없다

### 4.2 행위 중심 작성 원칙
- Given / When / Then 흐름이 테스트명에 자연스럽게 드러나야 한다.
- 하나의 테스트는 하나의 관찰 가능한 결과만 검증한다.

### 4.3 인증·권한 표시 규칙
인증이나 권한 조건이 있는 테스트는 접두어로 명시한다.

- 인증_: 로그인 상태가 전제 조건인 경우
- 권한_: 소유자/타인 구분이 필요한 경우
- 관리자_: 관리자 전용 기능인 경우
- 검증_: 입력값 검증 규칙인 경우
- 정책_: 404/403, 누적/중복 등 정책 결정이 포함된 경우

예:
- 인증_로그인한_사용자는_장바구니를_조회할_수_있다
- 관리자_상품을_등록할_수_있다
- 권한_댓글_작성자만_댓글을_삭제할_수_있다

---

## 5. Definition of Done (완료 기준)
test_list.md의 항목 하나를 완료로 처리하려면 다음을 만족해야 한다.

- 해당 항목을 검증하는 테스트가 존재한다.
- 테스트는 실패(Red) 상태에서 시작해 통과(Green)시켰다.
- 통과 후 리팩터링을 거쳐 구조가 정리되었다.
- 관련 API는 문서(drfspectacular schema)에 반영된다.

---

## 6. TDD 진행 규칙 (Kent Beck 방식)
- test_list.md에서 가장 쉬운 테스트 하나를 선택한다.
- 한 번에 하나의 테스트만 Red 상태로 만든다.
- 테스트를 통과시키는 최소 구현으로 Green을 만든다.
- 구조 개선은 Refactor 단계에서만 수행한다.
- 구조 변경 커밋과 행위 변경 커밋을 분리한다.

---

## 7. 단계별 진행 계획

### Phase 0: 부팅 및 기반
목표: 개발을 시작할 수 있는 안정적인 환경 확보
- 서버 실행(runserver) 가능
- pytest 실행 가능
- API schema/docs 접근 가능

완료 기준:
- 서버 부팅 오류 없음
- 테스트 0개 상태에서도 pytest 정상 실행

---

### Phase 1: Users (가입/로그인)
목표: 인증이 가능한 상태 확보
- 회원가입
- 로그인 및 토큰 발급
- 인증 필요 API 보호 정책 확정

완료 기준:
- test_list.md의 Users 관련 테스트 전부 통과

---

### Phase 2: Products
목표: 상품 카탈로그 조회 가능
- 메뉴/카테고리/상품 목록 및 상세
- 페이징/정렬 정책 확정
- 관리자 상품 등록

완료 기준:
- test_list.md의 Products 관련 테스트 전부 통과

---

### Phase 3: Cart
목표: 인증 기반 장바구니 기능 제공
- 조회/담기/수정/삭제
- 수량 누적 정책 확정
- 타인 장바구니 접근 차단 정책 확정

완료 기준:
- test_list.md의 Cart 관련 테스트 전부 통과

---

### Phase 4: Postings
목표: 후기 및 댓글 기능 제공
- 후기 작성
- 댓글 작성/삭제 및 권한 처리

완료 기준:
- test_list.md의 Postings 관련 테스트 전부 통과

---

### Phase 5: Backlog 정합성 확보
목표: 기존 문서 기능과의 정합성 확보
- Users 상세 필드 확장 (username, mobile_number 등)
- Products 상세 도메인/메인 목록 보강
- Cart 상세 상품 기반 구조 확장
- Wishlist 제공 여부 결정 및 반영

완료 기준:
- test_list.md의 Backlog 항목 중 P1 전부 통과

---

## 8. 참고 문서
- test_list.md: 검증해야 할 전체 테스트 목록
