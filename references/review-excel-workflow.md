# Review Excel Workflow

Use this workflow whenever the user provides a review Excel or CSV.

## Goal

Create a vivid customer-review cut from real reviews:

- Most recent 1 month if a date column exists.
- Most positive and concrete snippets.
- Exactly 5 review bubbles/cards.
- 4 customer-fit USP checkbox points based on review patterns and product facts.

## Accepted Columns

Try to detect these columns automatically:

- Review text: `리뷰내용`, `내용`, `후기`, `review`, `comment`
- Rating: `리뷰점수`, `평점`, `별점`, `rating`, `score`
- Date: `리뷰날짜`, `작성일`, `등록일`, `date`, `created_at`
- User: `작성자`, `아이디`, `닉네임`, `user`, `username`

If the date column is missing, say that the recent-1-month filter could not be verified and use the most positive available reviews.

## Helper Script

Prefer:

```bash
python scripts/analyze_reviews.py reviews.xlsx --out output/review-analysis.json --top 5 --days 30
```

Resolve the script path from the skill folder. Do not search unrelated current working directories for review tools.

## Review Cut Copy Rules

The review image must include:

1. 5 review bubbles/cards with masked user ids.
2. A small source/disclaimer line:
   `* 활용 동의를 받은 자사 실 제품 구매 리뷰 발췌, 개인차 있음.`
3. Heading:
   `우리 제품 이런분께 추천 드려요!`
4. 4 rectangular checkbox USP points.
5. Bottom CTA:
   `지금 바로 경험해보세요!`

## USP Extraction

Create USP checkbox points from repeated review themes and confirmed product facts.

Good:

- `피부가 힘 없이 축 처진 느낌이 들어요`
- `눈가, 이마 등 부위별 주름 관리가 시급해요`
- `순하게 쓸 수 있는 주름 크림 없을까요?`

Avoid:

- Unsupported medical effects.
- Guaranteed outcomes.
- Numeric performance claims without evidence.
- Any claim not present in reviews or product facts.

## If Reviews Are Missing

Do not invent reviews. In the plan, mark `리뷰 엑셀 확인 필요` and ask the user to upload the file before final image generation.
