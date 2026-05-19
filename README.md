# Danah Image-Cut Detail Page

> 단아쌤 쇼핑몰 학교 [https://shoppingmallschool.com](https://shoppingmallschool.com)
> Korean ecommerce detail-page skill for ChatGPT Codex.
> MIT License - 자유롭게 사용, 수정, 재배포할 수 있습니다. 단, 저작권 표기는 유지해주세요.

---

`danah-image-cut-detail-page`는 쿠팡, 네이버 스마트스토어, 모바일 쇼핑몰용 상세페이지를 **긴 한 장 이미지가 아니라 여러 개의 판매용 이미지 컷**으로 기획하고 제작하도록 돕는 Codex 스킬입니다.

제품 사진, 리뷰 엑셀, 상품정보제공고시 자료를 바탕으로 상세페이지 컷 구조를 먼저 기획한 뒤, 승인된 컷 계획에 맞춰 `section-01.png`, `section-02.png`처럼 개별 이미지를 생성하는 흐름을 따릅니다.

## 이런 분께 좋아요

- 쿠팡, 스마트스토어, 자사몰 상세페이지를 이미지 컷 단위로 만들고 싶은 분
- 리뷰 엑셀을 분석해서 구매 포인트와 신뢰 카피를 뽑고 싶은 분
- 상품정보제공고시, 배송 문구, 인증/효능 표현을 무리하게 꾸며내지 않고 안전하게 정리하고 싶은 분
- ChatGPT Codex에서 반복적으로 쓸 수 있는 상세페이지 제작 스킬이 필요한 분

## 주요 기능

- 10컷, 12컷, 18컷 상세페이지 구조 기획
- 쿠팡/스마트스토어에 맞는 컷 단위 흐름 설계
- 리뷰 엑셀 분석을 통한 긍정 문장과 구매 포인트 추출
- 상품정보제공고시 누락 항목 표시
- 컷별 헤드라인, 서브카피, 시각 연출 방향 작성
- Codex 이미지 생성 도구를 이용한 개별 컷 이미지 제작
- 최종 산출물 기준: `section-01.png`, `section-02.png` 등 분리 이미지

## 폴더 구조

```text
danah-image-cut-detail-page/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── cut-structure.md
│   ├── image-production.md
│   ├── planning-principles.md
│   ├── product-disclosure.md
│   └── review-excel-workflow.md
└── scripts/
    └── analyze_reviews.py
```

## 설치 방법

초보자도 아래 순서대로 진행하면 됩니다. Windows PowerShell 기준입니다.

### 1. Git 설치 확인

PowerShell에서 아래 명령어를 입력합니다.

```powershell
git --version
```

버전이 나오면 Git이 설치된 상태입니다. 설치되어 있지 않다면 [Git 공식 사이트](https://git-scm.com/downloads)에서 Windows용 Git을 먼저 설치하세요.

### 2. 스킬 다운로드

원하는 작업 폴더에서 아래 명령어를 실행합니다.

```powershell
git clone https://github.com/imteacherdana-sys/danha-detailpage.git
```

### 3. Codex 스킬 폴더로 복사

Codex에서 이 스킬을 항상 불러오려면 이 단계가 필요합니다.

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\danha-detailpage" "$env:USERPROFILE\.codex\skills\danah-image-cut-detail-page"
```

설치 후 폴더 위치는 보통 아래와 같습니다.

```text
C:\Users\사용자이름\.codex\skills\danah-image-cut-detail-page
```

참고: 다운로드한 폴더 안에서만 작업할 때는 복사하지 않아도 됩니다. 하지만 다른 프로젝트에서도 "단아쌤 상세페이지 만들어줘"라고 바로 쓰려면 스킬 폴더에 복사하는 것을 권장합니다.

### 4. Python 패키지 설치

리뷰 엑셀 분석 스크립트를 쓰려면 아래 패키지가 필요합니다.

```powershell
pip install pandas openpyxl
```

단순히 Codex가 `SKILL.md`를 읽고 상세페이지 컷 기획을 만드는 용도라면 이 단계는 나중에 해도 됩니다.

## 사용 방법

Codex에서 아래처럼 요청하세요.

```text
단아쌤 상세페이지 만들어줘.
제품 사진, 리뷰 엑셀, 상품정보제공고시 자료를 반영해서 12컷으로 만들어줘.
```

스킬은 먼저 필요한 자료를 확인합니다.

- 리뷰 엑셀 파일
- 제품 이미지
- 상품정보제공고시 이미지 또는 텍스트

자료가 부족해도 초안 기획은 가능하지만, 최종 판매용 이미지에서는 확인되지 않은 원산지, 인증, 효능, 배송 문구, 리뷰를 임의로 만들지 않습니다.

## 업데이트 방법

이미 설치한 뒤 새 버전을 받고 싶다면 다운로드한 폴더에서 아래 명령어를 실행합니다.

```powershell
git pull
Copy-Item -Recurse -Force ".\danha-detailpage" "$env:USERPROFILE\.codex\skills\danah-image-cut-detail-page"
```

## 라이선스

MIT License. 자유롭게 사용, 수정, 재배포할 수 있습니다. 단, 저작권 표기는 유지해야 합니다.

자세한 내용은 [LICENSE](LICENSE) 파일을 확인하세요.
