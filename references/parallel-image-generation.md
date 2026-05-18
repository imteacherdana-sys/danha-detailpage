# 병렬 이미지 생성 — 단아쌤 상세페이지 스킬

> 📦 단아쌤 한국형 상세페이지 스킬 · https://shoppingmallschool.com

12개 섹션 이미지를 하나씩 순차 생성하면 **약 5~8분**이 걸린다. 동시 병렬 생성하면 **30~60초**에 끝난다. 시간을 12배 단축하는 핵심 워크플로우다.

## 핵심 원칙

1. **호스트 에이전트는 코디네이터 역할만** — 직접 이미지를 만들지 않고, 컷마다 worker를 띄운다.
2. **컷당 worker 1개** — 12컷이면 12개 worker가 동시에 돈다.
3. **각 worker는 독립적** — 자기 컷만 생성, 다른 컷에 의존 X.
4. **launch 먼저, 대기 나중** — 12개 다 띄운 다음 결과를 기다린다. 1번 띄우고 기다리고 2번 띄우는 식 절대 금지.
5. **실패는 격리** — 한 worker 실패해도 다른 worker는 계속 진행. 끝난 후 실패한 컷만 재시도.

## Worker 인풋 (컷당 동일 구조)

```yaml
worker_input:
  cut_id: "section-01"                       # 컷 식별자
  cut_name: "후킹 / 일상 불편 공감"          # 사람이 읽는 이름
  prompt: "거실에서 자녀와 함께 사용하는 모먼트, 자연광, 라이프스타일 톤"
  reference_image: "./product.jpg"            # 제품 사진 (있으면)
  preserve_product: true                      # 외관 보존 모드
  ratio: "1:1"                                # 비율
  text_overlay: "이렇게 편한 세차의자, 진짜였어?"  # 이미지 안에 박을 한글 (선택, 8~15자)
  output_path: "./output/section-01.png"
  max_retries: 1                              # 실패시 1회 재시도
```

## 환경별 실제 실행 방법

### ChatGPT Codex 환경

Codex는 내장 병렬 워커 spawning을 지원한다. 한 응답 안에서 12개 이미지 생성을 동시 요청:

```
호스트 에이전트가 한 응답 안에서 12개의 이미지 생성 도구 호출을 동시에 발행한다.
각 호출은 독립적 — Codex 내부 스케줄러가 가능한 만큼 병렬로 처리.

⚠️ 순서대로 부르지 말 것. 한 응답에 12개 도구 호출을 묶어서 발행해야 진짜 병렬.
```

`agents/parallel.yaml` 의 `orchestration.max_concurrent` 값이 한 번에 띄울 수 있는 최대 worker 수를 정의.

### Claude Code 환경 (옵션)

Claude Code는 `Bash` 또는 Agent 도구로 백그라운드 실행 가능:

```bash
# 12개 컷을 동시에 백그라운드 실행
for i in $(seq -w 1 12); do
  python scripts/generate_image.py \
    --prompt "$(jq -r ".sections[$((10#$i - 1))].prompt" plan.json)" \
    --reference product.jpg \
    --ratio "$(jq -r ".sections[$((10#$i - 1))].ratio" plan.json)" \
    --out "output/section-${i}.png" &
done
wait  # 12개 모두 끝날 때까지 대기
```

또는 GNU `parallel` 사용:

```bash
seq -w 1 12 | parallel -j 12 python scripts/generate_image.py \
  --prompt "$(jq -r '.sections[{=$_-=1=}].prompt' plan.json)" \
  --reference product.jpg \
  --ratio "$(jq -r '.sections[{=$_-=1=}].ratio' plan.json)" \
  --out "output/section-{}.png"
```

## QA 단계 (병렬 후)

12개가 다 끝난 뒤 다음을 일괄 검증:

| 항목 | 통과 기준 | 실패 처리 |
|---|---|---|
| 파일 생성 여부 | 12개 모두 존재 | 누락 컷만 재실행 |
| 파일 크기 | 50KB 이상 (정상 PNG) | 작으면 재실행 |
| 제품 외관 일관성 | 모든 컷에서 같은 제품 | 다르면 사용자 알림 + 옵션 제공 |
| 한글 텍스트 (있는 컷) | 깨지지 않고 읽힘 | 깨졌으면 텍스트 단축 후 재실행 |

QA 실패 컷만 모아서 두 번째 병렬 배치로 재실행.

## 실패 처리 패턴

```
초기 배치: 12 컷 동시 launch
  ├─ 10 컷 성공
  └─ 2 컷 실패 (텍스트 깨짐)
재시도 배치: 실패한 2 컷만 동시 launch (프롬프트 강화)
  └─ 2 컷 모두 성공
최종: 12 / 12 완료
```

3회 시도 후에도 실패하는 컷은 사용자에게 알리고 옵션 제공:
- A. 텍스트 없이 이미지만 (텍스트는 HTML로 분리)
- B. 영문 프롬프트로 재시도
- C. 해당 컷 스킵

## 비용 의식

병렬이라고 해서 비용이 줄지 않는다 — 12장 만들면 12장 비용. 다만 **시간이 짧아지므로** 사용자가 검토·재시도할 여유가 생긴다.

Codex 환경에서는 ChatGPT 구독에 포함이라 사실상 무료. Claude Code + API 환경에서는 장당 비용 그대로.

## 호스트 에이전트 지시 예시

이 reference를 따라 SKILL.md STEP 7에서 다음과 같이 행동한다:

```
✅ 좋은 패턴:
"이제 12개 섹션 이미지를 동시에 생성하겠습니다."
[한 응답에 12개 이미지 생성 도구 호출 발행]

❌ 나쁜 패턴:
"섹션 1 이미지 생성 중..." [생성 완료까지 대기]
"이제 섹션 2..." [또 대기]
```
