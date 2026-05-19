# 단아쌤 한국형 상세페이지 스킬

> 📦 **단아쌤 개발** — 쇼핑몰스쿨 [https://shoppingmallschool.com](https://shoppingmallschool.com)
> 단아쌤이 10년간 다듬어 온 한국형 상세페이지 공식을 ChatGPT Codex에 그대로 옮긴 스킬
> MIT License — 자유롭게 사용·수정·재배포 가능 (저작권 표기 유지 필수)

---

ChatGPT Codex 안에서 한국형 상세페이지를 처음부터 끝까지 만드는 스킬입니다.
9개 카테고리 자동 매칭, 5개 보이스톤, AIDA+PAS 스토리텔링, 리뷰 기반 카피, 그리고 **Codex의 내장 이미지 생성 도구**(gpt-image-2 기반)로 제품 사진을 그대로 유지한 채 섹션별 이미지를 **병렬로** 생성합니다.

**별도 API key·결제 등록 필요 없음** — ChatGPT 구독에 모두 포함됩니다.

## 핵심 강점 5가지

1. **9개 카테고리 × 93개 섹션 스키마** — 카테고리마다 정확히 어떤 섹션이 어떤 순서로 들어가야 하는지 JSON으로 박혀있음
2. **5개 보이스톤** — 와디즈식 자극 / 전문가·실용 / 프리미엄·고급 / 친근·라이프스타일 / 트렌디·활기찬
3. **AIDA+PAS 자동 태깅** — 모든 섹션에 마케팅 스토리텔링 단계 표시
4. **병렬 이미지 생성** — 12장을 한 번에 동시 생성 (순차 대비 12배 빠름)
5. **컴플라이언스 자동 체크** — 카테고리별 식약처·KC·공정위 규정 자동 검토

## 사전 준비

```bash
# 로컬 처리용 Python 의존성
pip install pandas openpyxl pillow
```

이게 전부입니다. 이미지 생성은 Codex가 자체 처리.

## 설치 (Codex)

초보자도 아래 순서대로 하면 설치할 수 있습니다. Windows PowerShell 기준입니다.

### 1. Git 설치 확인

PowerShell을 열고 아래 명령어를 입력합니다.

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

아래 명령어를 그대로 실행합니다.

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\danha-detailpage" "$env:USERPROFILE\.codex\skills\danha-detailpage"
```

설치 후 폴더 위치는 보통 아래와 같습니다.

```text
C:\Users\사용자이름\.codex\skills\danha-detailpage
```

### 4. 필요한 Python 패키지 설치

리뷰 엑셀 분석과 이미지 처리용으로 아래 패키지를 설치합니다.

```powershell
pip install pandas openpyxl pillow
```

### 5. Codex에서 사용하기

Codex를 다시 열고 아래처럼 요청하면 됩니다.

```text
단아쌤 상세페이지 만들어줘.
제품 사진은 product_01.png부터 product_06.png까지 있고, 리뷰 엑셀도 반영해줘.
```

Codex가 이 스킬의 `SKILL.md`를 읽고 상세페이지 기획, 리뷰 분석, 이미지 컷 생성, 최종 HTML/갤러리 생성 순서로 안내합니다.

### 업데이트 방법

이미 설치한 뒤 새 버전을 받고 싶다면 다운로드한 폴더에서 아래 명령어를 실행합니다.

```powershell
git pull
Copy-Item -Recurse -Force ".\danha-detailpage" "$env:USERPROFILE\.codex\skills\danha-detailpage"
```

## 사용법

Codex 안에서:

> "이 제품으로 상세페이지 만들어줘. 사진은 `./product.jpg` 에 있어."
>
> "리뷰 엑셀(`reviews.xlsx`)도 같이 반영해서 와디즈식 후킹으로 짜줘."

Codex가 STEP 1~10을 자동 안내합니다.

## 폴더 구조 (모듈식)

```
danah-detail-page-skill/
├── SKILL.md                          # 오케스트레이션 (호스트가 읽음)
├── README.md                         # 사람용 가이드
├── LICENSE                           # MIT
├── .gitignore                        # 빌드 산출물 제외
│
├── data/                             # 구조화 데이터 (JSON)
│   ├── categories.json               # 9 카테고리 × 93 섹션 스펙
│   ├── voice-tones.json              # 5 보이스톤 가이드
│   ├── visual-tones.json             # 카테고리별 비주얼 톤 (한/영)
│   └── frameworks.json               # 4 스토리텔링 프레임워크
│
├── references/                       # 상세 워크플로우 (마크다운)
│   ├── intake-flow.md                # 인테이크 8개 질문 구조
│   ├── photo-quality-check.md        # 사진 품질 검수 분기
│   ├── category-compliance.md        # 카테고리별 식약처·KC 체크
│   ├── parallel-image-generation.md  # 병렬 이미지 생성 패턴
│   ├── final-image-standard.md       # 최종 이미지 QA 기준
│   └── output-format.md              # 출력 형식 규약
│
├── agents/
│   └── parallel.yaml                 # 병렬 worker 설정
│
└── scripts/                          # Python 헬퍼 (API 불필요)
    ├── parse_reviews.py              # 리뷰 xlsx → 긍정 문장 30개
    ├── render_html.py                # 최종 기획서 HTML
    ├── build_gallery.py              # 갤러리 HTML + 전체 ZIP
    └── generate_image.py             # [선택] Claude Code용 OpenAI API
```

## 9개 카테고리

| 카테고리 | 섹션 수 | 특징 |
|---|---|---|
| 💄 화장품 | 12 | 피부 고민 공감 → 성분·임상 → Before/After → 인증 → 전성분 |
| 👜 패션잡화 | 10 | 룩북 → 스타일링 3룩 → 디테일 매크로 → 사이즈 |
| 🏠 생활용품 | 9 | 일상 불편 공감 → 3특장점 → 사용 시나리오 → 경쟁 비교 |
| 🍱 식품 | 11 | 원재료 산지 → 제조 공정 → 영양 → 레시피 → HACCP |
| 🔌 전자제품 | 11 | 핵심 스펙 → 차별 기능 → 호환성 → 경쟁 스펙 → AS |
| 🧸 어린이용품 | 9 | 엄마 공감 → 안전성 → KC 인증 → 연령별 → 엄마 후기 |
| 🍳 주방용품 | 11 | 코팅 기술 → 조리 시나리오 → 세척 편의 → 내구 테스트 |
| 🧴 세제 | 10 | 얼룩 Before/After → 성분 안전 → 비교 실험 → 향 |
| 👕 의류 | 10 | 룩북 → 원단 디테일 → 사이즈 차트 → 키별 착용 |

## 5개 보이스톤

| 톤 | 타겟 | 예시 후킹 |
|---|---|---|
| 🔥 와디즈식 자극 | 모든 연령 / FOMO | "아직도 손 아프게 세차하세요?" |
| 🧠 전문가·실용 | 20~40대 남성 | "세차 시간 30% 단축" |
| 👑 프리미엄·고급 | 40대+ 고소득 | "당신의 세차를 위한 단 하나" |
| ☕ 친근·라이프스타일 | 30~40대 여성 | "오늘부터 세차가 편해집니다" |
| ✨ 트렌디·활기찬 | 20~30대 | "세차에도 꿀템이 필요하죠" |

## 워크플로우 10단계

자세한 내용은 [SKILL.md](SKILL.md) 의 "워크플로우" 섹션 참조.

| STEP | 단계 | 참조 |
|---|---|---|
| 0 | 자료 로드 | `data/*.json` |
| 1 | 제품 사진 분석 | `references/photo-quality-check.md` |
| 2 | 인테이크 (8 질문) | `references/intake-flow.md` |
| 3 | 제품 정보 보충 | (인라인) |
| 4 | 리뷰 엑셀 처리 (선택) | `scripts/parse_reviews.py` |
| 5 | 섹션별 카피 작성 | `references/output-format.md` |
| 6 | 카피 + 와이어프레임 승인 | (인라인) |
| 7 | **병렬 이미지 생성** | `references/parallel-image-generation.md` + `agents/parallel.yaml` |
| 8 | QA 패스 | `references/final-image-standard.md` |
| 9 | HTML 기획서 + 갤러리 출력 | `scripts/render_html.py` + `scripts/build_gallery.py` |
| 10 | 컴플라이언스 + 마무리 | `references/category-compliance.md` |

## 산출물

스킬 완료 후 `output/` 폴더에:

```
output/
├── 상세페이지_기획서.html     # 클라이언트 전달용
├── 이미지_갤러리.html          # 이미지 검토 + 컷별 다운로드
├── 이미지_전체.zip             # 12장 한 번에 다운
├── section-01.png ~ -12.png   # 개별 이미지
└── plan.json                  # 메타데이터 (재생산용)
```

## 비용

**Codex 환경 (권장)**
- ChatGPT 구독료(Plus/Pro/Team)에 모두 포함
- API 종량제 청구 없음
- 구독 등급별 일일 이미지 한도가 있을 수 있음

**Claude Code + OpenAI API 환경 (선택)**
- `scripts/generate_image.py` 호출시 OpenAI 종량제
- gpt-image-2 단가는 https://openai.com/api/pricing/ 참조

## ai싱크 스킬과의 차별점

이 스킬은 [ai싱크 클럽의 ecommerce-detail-page 스킬](https://github.com/aisyncclub/detail_page_codex_skill)에서 영감 받은 **모듈식 아키텍처 패턴**(references 분리, 병렬 이미지 생성, 사진 품질 분기, HTML 갤러리)을 차용했지만, **콘텐츠는 전부 단아쌤 본인 자료**(v0.3.2 HTML 자동생성기·DOCX 사용 가이드)에서 새로 짠 오리지널입니다.

| 항목 | ai싱크 | 단아쌤 |
|---|---|---|
| 카테고리 | 일반 9개 | **구체 9개 + 93 섹션 스키마** |
| 보이스톤 | 별도 개념 없음 | **5개 명시 + 자동 추천** |
| 스토리텔링 | 컷 흐름에 묻혀있음 | **AIDA+PAS 태그 명시** |
| 리뷰 처리 | 없음 | **xlsx 파서 + 긍정 문장 추출** |
| 데이터 | 프로즈 마크다운 | **JSON 구조화** |
| 컴플라이언스 | 일반 가이드 | **카테고리별 식약처·KC 자동 체크** |
| 병렬 이미지 생성 | ✅ | ✅ |
| 갤러리 + ZIP | ✅ | ✅ |
| 모듈식 references | ✅ | ✅ |

## v0.3.2 HTML 자동생성기와의 관계

브라우저 도구 [한국형 상세페이지 기획서 자동생성기 v0.3.2](../한국형_상세페이지_기획서_자동생성기_v0.3.html)의 카피 템플릿·레이아웃 플로우·보이스톤 지시를 ChatGPT Codex 환경에 맞게 재구성한 버전.

| 항목 | v0.3.2 HTML (브라우저) | 이 스킬 (Codex) |
|---|---|---|
| 카피 생성 | Gemini 2.5 Flash | Codex (GPT 계열) |
| 이미지 생성 | Nano Banana (Gemini) | **Codex 내장 gpt-image-2** |
| 이미지 처리 | 순차 1장씩 | **병렬 12장 동시** |
| UI | 브라우저 폼 | Codex 대화 |
| API key | Gemini 키 필요 | **불필요** (구독 포함) |

## 스크립트 직접 실행 (선택)

```bash
# 리뷰 엑셀 → 긍정 문장 추출
python scripts/parse_reviews.py reviews.xlsx --out output/reviews.json --top 30

# 최종 HTML 기획서
python scripts/render_html.py --plan output/plan.json --out output/상세페이지_기획서.html

# 이미지 갤러리 + 전체 ZIP
python scripts/build_gallery.py --plan output/plan.json --images-dir output --out output/이미지_갤러리.html
```

## 트러블슈팅

**Q. Codex에서 이미지가 순차로 생성돼요. 병렬이 안 돼요.**
A. `references/parallel-image-generation.md` 의 "호스트 에이전트 지시 예시" 부분을 Codex가 따라야 합니다. 한 응답 안에 12개 이미지 생성 도구 호출을 동시 발행해야 진짜 병렬. "이미지 12장을 동시에 생성해주세요" 라고 명시 지시하면 됩니다.

**Q. 한국어 텍스트가 이미지에 잘 들어가요?**
A. gpt-image-2부터 멀티링구얼 텍스트 렌더링이 강화되어 한글도 잘 박힙니다. 짧은 후킹(8~15자)은 이미지에 박아도 OK. 본문은 HTML 텍스트로 분리.

**Q. 제품이 컷마다 다르게 나와요.**
A. 사진 reference가 제대로 전달되지 않은 경우. `references/parallel-image-generation.md` 의 worker_input 형식 확인. `preserve_product: true` 필수.

**Q. 인쇄해서 PDF 만들고 싶어요.**
A. `상세페이지_기획서.html` 더블클릭 → 브라우저에서 인쇄 (Ctrl+P) → "대상: PDF로 저장".

**Q. Claude Code에서 쓰고 싶어요.**
A. 가능합니다만 이미지 자동 생성은 안 됩니다. 두 가지 방법:
- 방법 A: STEP 7만 Codex로 가서 수동 생성 후 이미지 경로를 Claude Code에 알려주고 STEP 8~10 계속
- 방법 B: `scripts/generate_image.py` + `OPENAI_API_KEY` 환경변수 (Organization Verification 필요)

## 기여

버그 리포트·개선 제안 환영합니다. PR 환영. 자세한 한국형 이커머스 노하우는 [쇼핑몰스쿨](https://shoppingmallschool.com)에서.

## 라이선스

MIT License. 자유롭게 사용·수정·재배포 가능. 단, 저작권 표기(`Copyright (c) 2026 단아쌤 · 쇼핑몰스쿨`)는 유지해야 합니다.

자세한 내용은 [LICENSE](LICENSE) 파일 참조.
