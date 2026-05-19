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

GitHub를 처음 쓰는 분은 **ZIP 다운로드 방식**을 추천합니다. Git을 설치하지 않아도 됩니다.

### 1. 스킬 ZIP 다운로드

1. 아래 GitHub 주소를 엽니다.
   [https://github.com/imteacherdana-sys/danha-detailpage](https://github.com/imteacherdana-sys/danha-detailpage)
2. 초록색 `Code` 버튼을 누릅니다.
3. `Download ZIP`을 누릅니다.
4. 내려받은 `danha-detailpage-main.zip` 파일을 찾습니다. 보통 `다운로드` 폴더에 있습니다.

### 2. 압축 풀기

압축은 찾기 쉬운 곳에 풀면 됩니다. 예를 들어 `문서` 폴더 아래에 아래처럼 풀어두면 관리하기 쉽습니다.

```text
C:\Users\사용자이름\Documents\CodexSkills\danha-detailpage-main
```

압축을 풀었을 때 그 안에 아래 파일이 보이면 정상입니다.

```text
SKILL.md
README.md
references
scripts
agents
```

### 3. Codex 스킬 폴더에 넣기

Codex가 이 스킬을 자동으로 알아보게 하려면 압축을 푼 폴더를 Codex 스킬 폴더로 복사해야 합니다.

최종 위치는 아래처럼 맞추는 것을 추천합니다.

```text
C:\Users\사용자이름\.codex\skills\danah-image-cut-detail-page
```

가장 쉬운 방법은 파일 탐색기에서 직접 복사하는 것입니다.

1. `danha-detailpage-main` 폴더를 엽니다.
2. 그 안의 파일과 폴더 전체를 복사합니다.
3. 아래 폴더를 만듭니다.

```text
C:\Users\사용자이름\.codex\skills\danah-image-cut-detail-page
```

4. 만든 폴더 안에 붙여넣습니다.

붙여넣은 뒤 아래처럼 보여야 합니다.

```text
C:\Users\사용자이름\.codex\skills\danah-image-cut-detail-page\SKILL.md
C:\Users\사용자이름\.codex\skills\danah-image-cut-detail-page\README.md
C:\Users\사용자이름\.codex\skills\danah-image-cut-detail-page\references
C:\Users\사용자이름\.codex\skills\danah-image-cut-detail-page\scripts
```

### 4. Codex에서 작업할 폴더 만들기

스킬을 설치한 폴더와 실제 상세페이지 작업 폴더는 다르게 쓰는 것이 좋습니다.

예를 들어 제품별 작업 폴더를 이렇게 만듭니다.

```text
C:\Users\사용자이름\Documents\CodexWork\참외상세페이지
```

이 작업 폴더 안에 제품 사진, 리뷰 엑셀, 상품정보제공고시 자료를 넣습니다.

```text
참외상세페이지
├── product_01.png
├── product_02.png
├── reviews.xlsx
└── 상품정보제공고시.png
```

그 다음 Codex에서 이 작업 폴더를 열고 요청하면 됩니다.

```text
단아쌤 상세페이지 만들어줘.
이 폴더에 있는 제품 사진, 리뷰 엑셀, 상품정보제공고시 자료를 반영해서 12컷으로 만들어줘.
```

### 5. Python 패키지 설치

리뷰 엑셀 분석 스크립트를 쓰려면 아래 패키지가 필요합니다.

```powershell
pip install pandas openpyxl
```

단순히 Codex가 `SKILL.md`를 읽고 상세페이지 컷 기획을 만드는 용도라면 이 단계는 나중에 해도 됩니다.

## Git을 아는 사용자를 위한 설치

Git을 사용할 줄 안다면 아래 방식으로 받을 수도 있습니다.

```powershell
git clone https://github.com/imteacherdana-sys/danha-detailpage.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\danha-detailpage" "$env:USERPROFILE\.codex\skills\danah-image-cut-detail-page"
```

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

ZIP으로 설치했다면 새 버전이 필요할 때 GitHub에서 ZIP을 다시 다운로드한 뒤 같은 위치에 덮어씌우면 됩니다.

Git으로 설치했다면 다운로드한 폴더에서 아래 명령어를 실행합니다.

```powershell
git pull
Copy-Item -Recurse -Force ".\danha-detailpage" "$env:USERPROFILE\.codex\skills\danah-image-cut-detail-page"
```

## 라이선스

MIT License. 자유롭게 사용, 수정, 재배포할 수 있습니다. 단, 저작권 표기는 유지해야 합니다.

자세한 내용은 [LICENSE](LICENSE) 파일을 확인하세요.
