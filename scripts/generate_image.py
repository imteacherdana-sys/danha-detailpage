"""
gpt-image-2 이미지 생성 — 단아쌤 상세페이지 스킬

📦 단아쌤 개발 · 쇼핑몰스쿨 https://shoppingmallschool.com
   MIT License — 자유롭게 사용·수정·재배포 가능 (저작권 표기 유지)

OpenAI gpt-image-2 (2026.04 출시) 기반.
- 임의 해상도 지원 (3:1 ~ 1:3 범위)
- 멀티링구얼 텍스트 렌더링 (한글 직접 박기 가능)
- 에이전틱 추론 (이미지 구조 사전 plan)

제품 사진이 reference로 주어지면 images/edits 엔드포인트로 전송해
제품 외관(색·로고·형태)을 유지한 채 배경·연출만 재구성한다.
reference 없으면 images/generations 으로 텍스트 전용 생성.

사전 준비:
  pip install openai pillow
  $env:OPENAI_API_KEY = "sk-..."   # PowerShell
  export OPENAI_API_KEY=sk-...     # bash

  ※ OpenAI 콘솔에서 'API Organization Verification' 필요할 수 있음.
    GPT Image 계열은 게이팅되어 있어 첫 호출 전에 인증 절차를 마쳐야 한다.

사용법:
  python generate_image.py \
    --prompt "거실에서 자녀와 함께 사용하는 모먼트, 자연광" \
    --reference product.jpg \
    --ratio 1:1 \
    --out output/section-01.png

종료 코드:
  0 = 성공
  2 = API 키 미설정
  3 = 입력 오류
  4 = API 호출 실패
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
from pathlib import Path

# gpt-image-2는 임의 해상도 지원 (3:1 ~ 1:3 범위). 정확한 비율로 매핑.
# 한 변은 2048까지, 짧은 변은 비율에 맞춰 자동 결정.
RATIO_TO_SIZE = {
    "1:1":  "1024x1024",
    "4:5":  "1024x1280",   # 진짜 4:5 (gpt-image-2부터 정확히 가능)
    "5:4":  "1280x1024",
    "3:4":  "1024x1365",
    "4:3":  "1365x1024",
    "16:9": "1820x1024",   # 진짜 16:9 (긴 변 1820)
    "9:16": "1024x1820",
    "3:1":  "2048x683",    # 최대 가로
    "1:3":  "683x2048",    # 최대 세로
    "auto": "auto",
}

PRODUCT_PRESERVE_INSTRUCTION_KO = (
    "이 이미지에 보이는 제품 자체(색상·로고·형태·재질)는 절대 바꾸지 마세요. "
    "오직 배경, 조명, 연출, 소품, 모델 동작만 다음 컨셉에 맞게 재구성하세요: "
)

PRODUCT_PRESERVE_INSTRUCTION_EN = (
    "Keep the product itself (color, logo, shape, material) exactly as shown in the reference image. "
    "Only the background, lighting, styling, props, and model action should be reconstructed to match this concept: "
)


def is_korean(text: str) -> bool:
    return any("가" <= c <= "힣" for c in text)


def build_prompt(user_prompt: str, has_reference: bool) -> str:
    if not has_reference:
        return user_prompt
    if is_korean(user_prompt):
        return PRODUCT_PRESERVE_INSTRUCTION_KO + user_prompt
    return PRODUCT_PRESERVE_INSTRUCTION_EN + user_prompt


def get_client():
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai 패키지가 없습니다. `pip install openai` 먼저 실행하세요.", file=sys.stderr)
        sys.exit(3)
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("ERROR: OPENAI_API_KEY 환경변수가 비어있습니다.", file=sys.stderr)
        sys.exit(2)
    return OpenAI(api_key=key)


def generate_with_reference(client, prompt: str, reference_path: Path, size: str, quality: str, model: str):
    with open(reference_path, "rb") as ref:
        return client.images.edit(
            model=model,
            image=ref,
            prompt=prompt,
            size=size,
            quality=quality,
        )


def generate_without_reference(client, prompt: str, size: str, quality: str, model: str):
    return client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
    )


def save_image(response, out_path: Path) -> None:
    data = response.data[0]
    if getattr(data, "b64_json", None):
        out_path.write_bytes(base64.b64decode(data.b64_json))
        return
    if getattr(data, "url", None):
        import urllib.request
        urllib.request.urlretrieve(data.url, out_path)
        return
    raise RuntimeError("응답에 b64_json도 url도 없습니다.")


def main() -> int:
    print("📦 단아쌤 한국형 상세페이지 스킬 · https://shoppingmallschool.com")
    ap = argparse.ArgumentParser(description="gpt-image-2 이미지 생성 (단아쌤 상세페이지 스킬)")
    ap.add_argument("--prompt", required=True, help="이미지 프롬프트 (한국어 또는 영어)")
    ap.add_argument("--reference", help="제품 사진 경로 (제공시 외관 유지 모드)")
    ap.add_argument("--ratio", default="1:1", choices=list(RATIO_TO_SIZE.keys()), help="이미지 비율 (gpt-image-2는 3:1~1:3 범위 지원)")
    ap.add_argument("--quality", default="medium", choices=["low", "medium", "high", "auto"], help="품질 (medium 권장 — low는 약 30%% 저렴)")
    ap.add_argument("--model", default="gpt-image-2", help="모델 ID (기본 gpt-image-2, 스냅샷 지정시 gpt-image-2-2026-04-21)")
    ap.add_argument("--out", required=True, help="출력 파일 경로 (.png)")
    args = ap.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    size = RATIO_TO_SIZE[args.ratio]
    ref_path = Path(args.reference) if args.reference else None
    if ref_path and not ref_path.exists():
        print(f"ERROR: 레퍼런스 파일 없음: {ref_path}", file=sys.stderr)
        return 3

    full_prompt = build_prompt(args.prompt, has_reference=ref_path is not None)
    client = get_client()

    print(f"[generate_image] model={args.model} size={size} quality={args.quality} ref={'yes' if ref_path else 'no'}")
    try:
        if ref_path:
            resp = generate_with_reference(client, full_prompt, ref_path, size, args.quality, args.model)
        else:
            resp = generate_without_reference(client, full_prompt, size, args.quality, args.model)
    except Exception as e:
        print(f"ERROR: OpenAI API 호출 실패: {e}", file=sys.stderr)
        return 4

    save_image(resp, out_path)
    print(f"OK: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
