# 단아쌤 한국형 상세페이지 스킬

> 📦 **단아쌤 개발** — 쇼핑몰스쿨 [https://shoppingmallschool.com](https://shoppingmallschool.com)
> 단아쌤이 10년간 다듬어 온 한국형 상세페이지 공식을 ChatGPT Codex에 그대로 옮긴 스킬
> MIT License — 자유롭게 사용·수정·재배포 가능 (저작권 표기 유지 필수)

---

ChatGPT Codex 안에서 한국형 상세페이지를 처음부터 끝까지 만드는 스킬입니다.
9개 카테고리 자동 매칭, 5개 보이스톤, AIDA+PAS 스토리텔링, 리뷰 기반 카피, 그리고 **Codex의 내장 이미지 생성 도구**(gpt-image-2 기반)로 제품 사진을 그대로 유지한 채 섹션별 이미지를 생성합니다.

**별도 API key·결제 등록 필요 없음** — ChatGPT 구독에 모두 포함됩니다.

## 사전 준비

```bash
# 로컬 처리용 Python 의존성 (리뷰 파싱 + HTML 렌더링용)
pip install pandas openpyxl
```

이게 전부입니다. 이미지 생성은 Codex가 자체적으로 처리하므로 OpenAI API key 설정·신분 인증·결제카드 등록 모두 불필요합니다.

## 설치 (Codex)

이 폴더(`danah-detail-page-skill/`)를 작업 디렉터리에 통째로 두세요. Codex가 SKILL.md를 자동으로 인식합니다.

또는 Codex 워크스페이스의 `~/.codex/skills/` 같은 위치에 둬도 됩니다 (Codex 버전·설정에 따라 경로가 달라질 수 있어요).

## 사용법

Codex 안에서 다음과 같이 말하면 스킬이 자동 발동합니다.

> "이 제품으로 상세페이지 만들어줘. 사진은 `./product.jpg` 에 있어."
>
> "리뷰 엑셀(`reviews.xlsx`)도 같이 반영해서 와디즈식 후킹으로 짜줘."

이후 Codex가 STEP 1 ~ STEP 9를 자동으로 안내합니다.

## 폴더 구조

```
danah-detail-page-skill/
├── SKILL.md                    # 스킬 정의 (호스트 에이전트가 읽음)
├── README.md                   # 사람이 읽는 가이드
├── data/
│   ├── categories.json         # 9개 카테고리 × 93개 섹션 스펙
│   ├── voice-tones.json        # 5개 보이스톤
│   ├── visual-tones.json       # 카테고리별 비주얼 톤
│   └── frameworks.json         # AIDA+PAS / BAB / 영웅의 여정 / FAB
└── scripts/
    ├── parse_reviews.py        # 리뷰 엑셀 → 긍정 문장 상위 30개 (API 불필요)
    ├── render_html.py          # 최종 단일 HTML 기획서 출력 (API 불필요)
    └── generate_image.py       # [선택] Claude Code 자동화용 OpenAI API 호출 (API key 필요)
```

> **주요 흐름은 Codex 네이티브 이미지 도구 사용**이라 `generate_image.py`는 안 씁니다. Claude Code 같은 다른 환경에서 자동화하고 싶을 때만 옵션으로 제공.

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

## 비용

**Codex에서 쓰는 경우 (권장)**
- ChatGPT 구독료(Plus/Pro/Team) 안에 모두 포함
- 별도 API 종량제 청구 없음
- 단, ChatGPT 구독 등급별로 일일 이미지 생성 한도가 있을 수 있음 (예: Plus는 일 N장)

**Claude Code에서 generate_image.py로 자동화하는 경우 (선택)**
- OpenAI 종량제 API 호출 → 사용량만큼 청구
- gpt-image-2 단가는 OpenAI 공식 가격표 참조: https://openai.com/api/pricing/

## v0.3.2 HTML 자동생성기와의 관계

이 스킬은 단아쌤이 만든 [한국형 상세페이지 기획서 자동생성기 v0.3.2](../한국형_상세페이지_기획서_자동생성기_v0.3.html)(Gemini 기반 브라우저 도구)의 카피 템플릿·레이아웃 플로우·보이스톤 지시를 **ChatGPT Codex 환경에 맞게 재구성**한 버전입니다.

| 항목 | v0.3.2 HTML (브라우저) | 이 스킬 (Codex) |
|---|---|---|
| 카피 생성 | Gemini 2.5 Flash | Codex (GPT 계열) |
| 이미지 생성 | Nano Banana (Gemini) | **Codex 내장 gpt-image-2** |
| UI | 브라우저 폼 | Codex 대화 |
| 리뷰 처리 | 브라우저 내 JS | Python 스크립트 |
| 출력 | 단일 HTML | 단일 HTML (동일 포맷) |
| API key | Gemini 키 필요 | **불필요** (구독에 포함) |

브라우저에서 가볍게 돌리고 싶으면 v0.3.2 HTML, Codex 안에서 자동화·반복 작업하고 싶으면 이 스킬을 쓰면 됩니다.

## 스크립트 직접 실행 (선택)

이미지 생성은 Codex가 자동 처리하지만, 리뷰 파싱과 최종 HTML 렌더링은 Python 스크립트로 따로 돌릴 수도 있습니다.

```bash
# 리뷰 엑셀 → 긍정 문장 추출 (API 불필요)
python scripts/parse_reviews.py reviews.xlsx --out reviews.json --top 30

# 최종 HTML 기획서 (API 불필요)
python scripts/render_html.py --plan plan.json --out 기획서.html
```

## 트러블슈팅

**Q. Codex에서 이미지 생성이 안 돼요.**
A. ChatGPT 구독 등급을 확인하세요. Codex의 이미지 생성 도구는 Plus 이상에서 활성화되며, 등급별 일일 한도가 있을 수 있습니다. 그 외에는 "지금 다음 프롬프트로 이미지를 생성해주세요" 라고 명시적으로 지시하면 호출됩니다.

**Q. 제품이 원본과 다르게 나와요.**
A. 제품 사진을 reference로 전달했는지 확인하세요. SKILL.md의 STEP 7에서 "제품 자체(색·로고·형태·재질)는 그대로 유지" 지시를 자동 주입하지만, 드물게 미세 변형이 일어날 수 있어서 1~2회 재생성하면 개선됩니다.

**Q. 리뷰 엑셀의 컬럼명이 영어예요.**
A. `parse_reviews.py`는 `review`, `rating`, `score` 같은 영어 헤더도 자동 인식합니다. 안 되면 1행 컬럼명을 `리뷰내용`, `리뷰점수` 로 바꾸세요.

**Q. 한국어 텍스트가 이미지에 잘 들어가요?**
A. Codex의 내장 이미지 모델(gpt-image-2 기반)은 멀티링구얼 텍스트 렌더링이 강화되어 한글도 꽤 정확히 박힙니다. 짧은 후킹(8~15자)은 이미지에 박아도 OK. 다만 본문 같은 긴 한국어는 띄어쓰기·맞춤법이 가끔 어색할 수 있어서 핵심 후킹만 이미지에, 나머지는 HTML 텍스트로 두는 게 안전합니다.

**Q. Claude Code에서 쓰고 싶어요.**
A. 가능합니다만 이미지 생성은 자동이 안 됩니다. 두 가지 방법:
- **방법 A**: STEP 7만 ChatGPT/Codex로 가서 수동으로 생성한 뒤 이미지 경로를 Claude Code에 알려주고 STEP 8~10 계속
- **방법 B**: `scripts/generate_image.py` 로 자동화 (이 경우에만 OPENAI_API_KEY 설정 + Organization Verification 필요)
