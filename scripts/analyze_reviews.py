from __future__ import annotations

import argparse
import json
import re
from datetime import timedelta
from pathlib import Path


REVIEW_COLS = ["리뷰내용", "내용", "후기", "review", "comment", "Review", "Comment"]
RATING_COLS = ["리뷰점수", "평점", "별점", "rating", "score", "Rating", "Score"]
DATE_COLS = ["리뷰날짜", "작성일", "등록일", "date", "created_at", "Date"]
USER_COLS = ["작성자", "아이디", "닉네임", "user", "username", "User"]

POSITIVE_WORDS = [
    "좋아요", "좋습니다", "만족", "추천", "재구매", "최고", "편해요", "부드러워요",
    "촉촉", "탄력", "순해요", "자극없", "빠르", "깔끔", "예뻐요", "가성비",
    "배송", "흡수", "향", "효과", "맘에", "마음에", "잘", "꾸준히",
]
NEGATIVE_WORDS = ["별로", "실망", "불편", "반품", "교환", "최악", "아쉬", "자극", "트러블"]


def find_col(columns, candidates):
    lower_map = {str(c).lower(): c for c in columns}
    for cand in candidates:
        if cand in columns:
            return cand
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    for col in columns:
        name = str(col).lower()
        if any(cand.lower() in name for cand in candidates):
            return col
    return None


def split_sentences(text):
    if not isinstance(text, str):
        return []
    parts = re.split(r"[.!?\n\r。]+", text)
    return [p.strip() for p in parts if 8 <= len(p.strip()) <= 70]


def mask_user(value, fallback_index):
    if value is None or str(value).strip() == "" or str(value).lower() == "nan":
        return f"@user{fallback_index:02d}****"
    raw = re.sub(r"\s+", "", str(value))
    raw = raw.lstrip("@")
    return "@" + raw[:4] + "****"


def score_text(text, rating=None):
    score = 0
    if rating is not None:
        try:
            score += int(float(rating) * 2)
        except (TypeError, ValueError):
            pass
    score += sum(3 for word in POSITIVE_WORDS if word in text)
    score -= sum(5 for word in NEGATIVE_WORDS if word in text)
    if 14 <= len(text) <= 45:
        score += 4
    elif 46 <= len(text) <= 70:
        score += 2
    return score


def main():
    parser = argparse.ArgumentParser(description="Analyze review Excel/CSV for detail-page review cuts.")
    parser.add_argument("input", help="Review xlsx/csv path")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--top", type=int, default=5, help="Number of review snippets")
    parser.add_argument("--days", type=int, default=30, help="Recent day window when date column exists")
    args = parser.parse_args()

    import pandas as pd

    input_path = Path(args.input)
    if input_path.suffix.lower() == ".csv":
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)

    review_col = find_col(df.columns, REVIEW_COLS)
    rating_col = find_col(df.columns, RATING_COLS)
    date_col = find_col(df.columns, DATE_COLS)
    user_col = find_col(df.columns, USER_COLS)
    if review_col is None:
        raise SystemExit(f"Review text column not found. Columns: {list(df.columns)}")

    date_filter_used = False
    if date_col is not None:
        dates = pd.to_datetime(df[date_col], errors="coerce")
        latest = dates.max()
        if pd.notna(latest):
            cutoff = latest - timedelta(days=args.days)
            df = df.loc[dates >= cutoff].copy()
            date_filter_used = True

    candidates = []
    for idx, row in df.iterrows():
        rating = row[rating_col] if rating_col is not None else None
        for sent in split_sentences(row[review_col]):
            score = score_text(sent, rating)
            if score <= 0:
                continue
            candidates.append(
                {
                    "text": sent,
                    "user": mask_user(row[user_col] if user_col is not None else None, len(candidates) + 1),
                    "score": score,
                }
            )

    selected = []
    seen = set()
    for item in sorted(candidates, key=lambda x: x["score"], reverse=True):
        key = item["text"]
        if key in seen:
            continue
        seen.add(key)
        selected.append(item)
        if len(selected) >= args.top:
            break

    themes = []
    for word in POSITIVE_WORDS:
        count = sum(1 for item in candidates if word in item["text"])
        if count:
            themes.append({"keyword": word, "count": count})
    themes.sort(key=lambda x: x["count"], reverse=True)

    result = {
        "dateFilterUsed": date_filter_used,
        "selectedReviews": selected,
        "topThemes": themes[:12],
        "uspDrafts": [
            f"{theme['keyword']} 관련 만족 후기가 반복돼요" for theme in themes[:4]
        ],
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path} with {len(selected)} selected reviews.")


if __name__ == "__main__":
    main()
