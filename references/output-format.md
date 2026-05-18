# 최종 출력 형식 — 단아쌤 상세페이지 스킬

> 📦 단아쌤 한국형 상세페이지 스킬 · https://shoppingmallschool.com

스킬이 만드는 산출물 3종의 정확한 형식 규약.

## 🚫 절대 금지 — 커스텀 렌더링 스크립트 생성

호스트 에이전트(Codex)는 제품별로 새 렌더링 스크립트를 만들지 않는다. **반드시 기존 두 스크립트만 사용**:

| 산출물 | 사용할 스크립트 |
|---|---|
| `상세페이지_기획서.html` | `python scripts/render_html.py --plan output/plan.json --out output/상세페이지_기획서.html` |
| `이미지_갤러리.html` + `이미지_전체.zip` | `python scripts/build_gallery.py --plan output/plan.json --images-dir output --out output/이미지_갤러리.html` |

**금지 패턴**:
- ❌ `scripts/build_waxball_page.py`, `scripts/build_tomato_page.py` 같은 제품별 일회성 스크립트
- ❌ Python으로 HTML을 직접 string concat해서 출력
- ❌ Codex 응답 안에 HTML을 인라인으로 작성

**왜?** 매번 새 스크립트 만들면 (1) AIDA 태그가 또 나타나거나, (2) CSS 디자인이 매번 달라지거나, (3) 사용자 로컬 경로가 하드코딩되거나, (4) 한국형 표준 레이아웃이 무너집니다. 기존 두 스크립트는 단아쌤이 검증한 표준이에요.

**스타일 변경이 필요하면** — 기존 `scripts/render_html.py` 또는 `scripts/build_gallery.py` 를 직접 편집하고 모든 사용자가 그 변경의 혜택을 받게 한다.

---

## 🚫 절대 표시 금지 — AIDA/PAS/TRUST/ACTION 태그 배지

마케팅 스토리텔링 단계(`AIDA-A`, `AIDA-I`, `AIDA-D`, `PAS-P`, `PAS-S`, `TRUST`, `ACTION`)는 **카피 작성을 위한 내부 메타데이터**다. 사용자 눈에 보이는 출력물에는 **배지·라벨·텍스트 형태 모두 절대 표시하지 않는다.**

| 곳 | 태그 표시 |
|---|---|
| `data/categories.json` · `plan.json` | ✅ JSON 내부 — Claude/Codex가 톤 결정에 사용 |
| 채팅 응답 마크다운 (섹션 헤딩) | ❌ 표시 금지 — 섹션 이름만 |
| 최종 `상세페이지_기획서.html` | ❌ 표시 금지 — `<span class="tag">` 같은 거 만들지 말 것 |
| `이미지_갤러리.html` | ❌ 표시 금지 |
| 새로 생성하는 어떤 HTML/이미지/문서 | ❌ 표시 금지 |

**이유** — 이 태그는 카피라이터(Claude/Codex)가 "이 섹션은 욕구 자극용이니 강한 어휘로" 같은 판단을 하기 위한 도구일 뿐, 최종 소비자나 클라이언트가 볼 정보가 아니다. 배지로 노출하면 상세페이지 디자인이 깨지고 셀러도 어색해한다.

**호스트 에이전트가 별도 렌더링 스크립트를 새로 만들 때도 동일 원칙** — `section["tags"]` 를 읽어서 `<span>` 으로 출력하지 말 것.

## 1. 마크다운 기획서 (Claude/Codex 응답 내)

대화 중에 사용자에게 보여주는 마크다운. STEP 6 카피 승인 단계에서 출력.

```markdown
# {{제품명}} 상세페이지 기획서

## 메타 정보
- **카테고리**: {{카테고리 이모지 + 한글명}} ({{N}}섹션)
- **보이스톤**: {{이모지 + 톤 이름}}
- **프레임워크**: AIDA+PAS (기본)
- **타겟 고객**: {{타겟 한 줄}}
- **가격**: {{가격}} / **옵션**: {{옵션}}
- **참조 사진**: {{있음/없음}}

## 핵심 전략
{{2~3문장으로 이 상세페이지의 설득 전략 요약}}

---

## 섹션 1. {{섹션 이름}}
- **비율**: 1:1 / **슬롯 타입**: 연출
- **목적**: {{이 섹션의 마케팅 목적}}

### 후킹
{{15~25자 한 줄, 강렬한 후킹}}

### 본문
{{3~5줄 본문, 구체적 숫자·감각어}}

### 이미지 프롬프트
- 🇰🇷 한글: {{한국어 프롬프트}}
- 🇺🇸 영어: {{영어 프롬프트}}

### 이미지에 박힐 텍스트 (선택)
{{8~15자 짧은 카피, gpt-image-2가 이미지에 직접 렌더링}}

---

## 섹션 2. ...
(같은 형식 반복)

---

## ⚖️ 컴플라이언스 체크
- ✅ 의약품 오인 표현 없음
- ⚠️ "프리미엄" 표현 — 근거 명시 권장
- 📋 KC 인증번호 (확인 필요)

## 다음 단계
A. 이대로 이미지 생성 (12장)
B. 특정 섹션 수정 후 진행
C. 보이스톤 변경 후 전체 재작성
```

## 2. plan.json (스크립트 입력용 구조화 데이터)

`scripts/render_html.py` 와 `scripts/build_gallery.py` 가 읽는 JSON. 카피 승인 후 자동 생성.

```json
{
  "meta": {
    "productName": "차몰랑 세차의자",
    "productPrice": "59000",
    "productVariant": "블랙/그레이",
    "productTarget": "30~40대 가족 단위 자가 세차러",
    "category": "household",
    "categoryName": "🏠 생활용품",
    "voiceTone": "wadiz",
    "voiceToneName": "🔥 와디즈식 자극",
    "framework": "aida-pas",
    "keywords": ["허리부담", "장시간세차", "접이식", "수납간편"],
    "usps": ["1초 펼침", "10kg 견딤", "트렁크 슬림 수납", "방수 원단"],
    "referencePhoto": "./product.jpg",
    "generatedAt": "2026-05-18T10:30:00Z"
  },
  "sections": [
    {
      "id": "hook",
      "order": 1,
      "name": "후킹 / 일상 불편 공감",
      "tags": ["AIDA-A", "PAS-P"],
      "ratio": "1:1",
      "slotType": "연출",
      "purpose": "공감으로 시선 잡기",
      "hook": "아직도 손 아프게 세차하세요?",
      "body": "허리도 아프고 무릎도 아프고\n시간도 1시간씩 걸리고\n오늘부터 그만하셔도 됩니다.",
      "imgPromptKo": "한국 30대 남성이 거실 옆 차고에서 세차의자에 앉아 차를 닦는 모먼트, 자연광, 따뜻한 톤",
      "imgPromptEn": "30s Korean male sitting on a fold-out car-wash chair beside a garage, natural light, warm tone, lifestyle photography",
      "textOverlay": "이렇게 편한 세차 처음?",
      "imgPath": "output/section-01.png",
      "imgStatus": "generated",
      "imgSize": 248320,
      "qaResults": {
        "fileExists": true,
        "fileSizeOk": true,
        "ratioMatch": true,
        "koreanTextOk": true,
        "productConsistent": true
      }
    }
  ],
  "compliance": {
    "checked": true,
    "warnings": [
      {
        "section": "intro",
        "issue": "'프리미엄' 표현 — 근거 명시 권장",
        "severity": "warning"
      }
    ],
    "missingFacts": [
      "KC 인증번호"
    ]
  }
}
```

## 3. 최종 HTML 산출물 2종

### 3a. 기획서 HTML (`상세페이지_기획서.html`)

`scripts/render_html.py` 출력. 클라이언트에 그대로 전달하는 카드 레이아웃.

구성:
- **헤더**: 제품명 + 메타 정보 (카테고리·보이스톤·프레임워크·타겟·가격)
- **목차**: 섹션 N개 점프 링크
- **섹션 카드**: 좌측 후킹+본문, 우측 이미지, 하단 프롬프트 (접힘)
- **푸터**: "더 많은 한국형 상세페이지 노하우: shoppingmallschool.com"

스타일:
- Pretendard 폰트
- 보라/핑크 그라데이션 헤더
- 카드 그림자 부드럽게
- 모바일 반응형

### 3b. 이미지 갤러리 HTML (`이미지_갤러리.html`)

`scripts/build_gallery.py` 출력. **이미지 다운로드 중심** 페이지.

구성:
- 헤더: 제품명 + 컷 수 + "전체 다운로드" 큰 버튼
- 그리드: 12장 썸네일, 각각:
  - 컷 번호 + 이름
  - 이미지 (썸네일, 클릭시 원본)
  - 비율 + 슬롯 타입 배지
  - "다운로드" 버튼 (개별)
  - QA 상태 (✅/⚠️/❌)

"전체 다운로드" 버튼:
- 같은 폴더의 `이미지_전체.zip` 으로 링크 (스크립트가 자동 생성)
- ZIP 안에 `section-01.png` ~ `section-12.png` + `index.txt` (컷 이름 매핑)

스타일:
- 다크모드 친화 (이미지 강조)
- 큰 썸네일 (가로 4열 데스크탑, 2열 태블릿, 1열 모바일)

## 파일 명명 규칙

```
output/
├── section-01.png         # zero-padded, 2자리
├── section-02.png
├── ...
├── section-12.png
├── 이미지_전체.zip          # build_gallery.py가 생성
├── 상세페이지_기획서.html    # render_html.py 출력
├── 이미지_갤러리.html        # build_gallery.py 출력
└── plan.json              # 모든 메타데이터
```

## 출력 폴더 정리

스킬 마지막에 사용자에게 다음을 안내:

```
✅ 모든 산출물이 다음 폴더에 있습니다:

📁 ./output/
├── 📄 상세페이지_기획서.html  ← 클라이언트 전달용
├── 📄 이미지_갤러리.html       ← 이미지 검토 + 다운로드
├── 📦 이미지_전체.zip          ← 12장 한 번에
├── 🖼 section-01.png ~ section-12.png
└── 📋 plan.json (메타데이터)

→ '상세페이지_기획서.html' 을 더블클릭하면 브라우저에서 바로 열립니다.
→ 인쇄 → 'PDF로 저장'으로 PDF 추출 가능.
→ 더 많은 노하우: https://shoppingmallschool.com
```
