# pure Django vs DRF 명시성 비교 (도메인별)

이 문서는 `25-1st-SPAOGAME-backend`(pure Django)와 현재 DRF 프로젝트를
도메인별로 비교하고, 명시성을 높이기 위한 리팩토링 방향을 정리한다.

---

## 1) Users

### pure Django 특징
- 입력 필드가 뷰에 직접 드러남 (username, mobile_number, address 등)
- 정규식 검증, 중복 검사, 해시 처리, 에러 응답이 한 파일에 모여 있음

### 현재 DRF 특징
- 입력 스키마가 축약됨 (email/password/name)
- 검증이 Serializer와 Django validator에 분산
- 응답 스키마/에러 포맷이 DRF 기본 형태에 의존

### 명시성 저하 요인
- 요구 필드가 문서 대비 축소되면서 “무엇을 받는지”가 단순화됨
- 검증 로직이 프레임워크 기본 동작에 숨겨짐

### 개선 방향
- Users 상세 필드 확장 (Backlog P1)
- 회원가입 입력 스키마를 Serializer에 명시적으로 정의
- 에러 포맷 통일 (예: {"error": "...", "code": "..."})

---

## 2) Products

### pure Django 특징
- Menu/Category/Product 생성과 조회 로직이 뷰에 직접 노출
- 색상/사이즈/이미지/상세상품(DetailedProduct) 모델을 활용
- 상품 상세에 리뷰/댓글 정보까지 조합하여 응답

### 현재 DRF 특징
- Menu/Category/Product의 기본 CRUD 일부만 제공
- 색상/사이즈/이미지/상세상품 개념이 없음
- 상품 상세는 단순 모델 필드만 반환

### 명시성 저하 요인
- 도메인 모델 축소로 인해 “상품 구성”이 드러나지 않음
- 상세 응답 조합 로직이 사라져 API 의도가 약해짐

### 개선 방향
- Color/Size/Image/DetailedProduct 도입 (Backlog P1)
- 상품 상세 응답에 상세 구성 및 리뷰/댓글 집계 포함 (Backlog P2)
- 조회 조합 로직은 Selector로 분리하여 명시적 구조 유지

---

## 3) Orders (Cart)

### pure Django 특징
- Cart가 상세 상품(DetailedProduct) 기반
- 색상/사이즈 입력, 중복 방지/존재 확인 정책이 뷰에 노출
- 요청/응답 스키마가 파일에서 바로 파악 가능

### 현재 DRF 특징
- CartItem이 Product 기반 (색상/사이즈 없음)
- 수량 검증 일부만 추가됨
- 정책 로직이 뷰에 섞여 있으며 구조 분리 미흡

### 명시성 저하 요인
- 상세 상품 기반 구조 부재
- 정책(중복/수량/존재) 기준이 분산되거나 누락

### 개선 방향
- Cart를 DetailedProduct 기반으로 재설계 (Backlog P1)
- 장바구니 정책을 Service로 이동
- 입력 검증은 Serializer에서 명시

---

## 4) Postings

### pure Django 특징
- 후기/댓글 생성 로직과 에러 처리가 뷰에 직접 노출
- 댓글 삭제 정책이 단순 (소유권 검증 없음)

### 현재 DRF 특징
- 후기/댓글 생성이 존재
- 댓글 삭제 시 소유권 검증 존재 (정책은 명시적)
- 대상 존재 검증 추가됨

### 명시성 저하 요인
- 요청 필드가 문서 기준과 다름 (review_content vs content 등)
- 조회 기능이 없어서 도메인 흐름이 끊겨 보임

### 개선 방향
- 요청 스키마를 문서/테스트와 맞추어 명시
- 후기/댓글 조회 추가 시 Selector로 분리

---

## 리팩토링 원칙 (명시성 중심)

1. **입력/출력 스키마를 Serializer로 명시**
2. **비즈니스 규칙은 Service로 이동**
3. **조회 조합은 Selector로 분리**
4. **에러 응답 포맷 통일**
5. **문서 기준 도메인 모델 복원**

