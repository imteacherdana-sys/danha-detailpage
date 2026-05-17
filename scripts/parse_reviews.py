"""
리뷰 엑셀 파싱 — 단아쌤 상세페이지 스킬

📦 단아쌤 개발 · 쇼핑몰스쿨 https://shoppingmallschool.com
   MIT License — 자유롭게 사용·수정·재배포 가능 (저작권 표기 유지)

스마트스토어·쿠팡·자체몰에서 내려받은 리뷰 엑셀을 받아서
4점 이상 리뷰 중 긍정 키워드를 포함한 12~60자 문장을 가중치 순 상위 30개 추출한다.

기대하는 컬럼 헤더 (한글):
  - 리뷰내용 (필수)
  - 리뷰점수 (필수)
  - 구매id, 리뷰날짜, 구매옵션, 수량 (선택)

영어 헤더(review/rating)도 자동 인식 시도.

사용법:
  pip install pandas openpyxl
  python parse_reviews.py reviews.xlsx --out reviews.json --top 30
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


POSITIVE_KEYWORDS = [
    # 일반 만족
    "좋아요", "좋습니다", "추천", "만족", "최고", "굿", "예뻐요", "이뻐요", "괜찮아요",
    # 효과·성능
    "효과", "잘 돼요", "잘되요", "잘 됩니다", "빨라요", "튼튼", "오래", "선명",
    # 사용 경험
    "편해요", "편리", "간편", "쉬워요", "가벼워요", "부드러워", "쫄깃", "촉촉",
    # 가성비·재구매
    "가성비", "가격대비", "재구매", "또 살", "또 사야", "강추",
    # 감성
    "선물", "마음에 들어", "기분 좋", "감동",
]

NEGATIVE_HINTS = [
    "별로", "아쉬", "실망", "최악", "별루", "안 좋", "안좋", "불편", "환불", "교환", "반품",
]

REVIEW_COL_CANDIDATES = ["리뷰내용", "내용", "후기", "review", "Review", "comment"]
RATING_COL_CANDIDATES = ["리뷰점수", "점수", "평점", "별점", "rating", "Rating", "score"]


def find_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    # case-insensitive partial
    for col in df.columns:
        lc = str(col).lower()
        for cand in candidates:
            if cand.lower() in lc:
                return col
    return None


def score_snippet(text: str) -> int:
    """가중치 — 긍정 키워드 매칭 수 + 적정 길이 보너스."""
    if not isinstance(text, str):
        return 0
    if any(neg in text for neg in NEGATIVE_HINTS):
        return 0
    n = sum(1 for k in POSITIVE_KEYWORDS if k in text)
    if n == 0:
        return 0
    length_bonus = 2 if 20 <= len(text) <= 50 else (1 if 12 <= len(text) <= 60 else 0)
    return n * 2 + length_bonus


def split_sentences(text: str) -> list[str]:
    if not isinstance(text, str):
        return []
    parts = re.split(r"[.!?。！？\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def main() -> int:
    print("📦 단아쌤 한국형 상세페이지 스킬 · https://shoppingmallschool.com")
    ap = argparse.ArgumentParser(description="리뷰 엑셀 파싱 (단아쌤 상세페이지 스킬)")
    ap.add_argument("xlsx", help="리뷰 xlsx 또는 csv 경로")
    ap.add_argument("--out", required=True, help="출력 JSON 경로")
    ap.add_argument("--top", type=int, default=30, help="상위 N개 (기본 30)")
    ap.add_argument("--min-rating", type=float, default=4.0, help="최소 점수 (기본 4점)")
    args = ap.parse_args()

    try:
        import pandas as pd
    except ImportError:
        print("ERROR: pandas가 필요합니다. `pip install pandas openpyxl`", file=sys.stderr)
        return 3

    path = Path(args.xlsx)
    if not path.exists():
        print(f"ERROR: 파일 없음: {path}", file=sys.stderr)
        return 3

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)

    review_col = find_column(df, REVIEW_COL_CANDIDATES)
    rating_col = find_column(df, RATING_COL_CANDIDATES)
    if not review_col:
        print(f"ERROR: 리뷰내용 컬럼을 찾을 수 없습니다. 컬럼: {list(df.columns)}", file=sys.stderr)
        return 3

    snippets: list[dict] = []
    for _, row in df.iterrows():
        if rating_col:
            try:
                if float(row[rating_col]) < args.min_rating:
                    continue
            except (ValueError, TypeError):
                pass
        text = row[review_col]
        for sent in split_sentences(text):
            if not (12 <= len(sent) <= 60):
                continue
            score = score_snippet(sent)
            if score > 0:
                snippets.append({"text": sent, "score": score})

    seen = set()
    deduped = []
    for s in sorted(snippets, key=lambda x: -x["score"]):
        if s["text"] in seen:
            continue
        seen.add(s["text"])
        deduped.append(s)
        if len(deduped) >= args.top:
            break

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(deduped, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {len(deduped)} 문장 추출 → {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
