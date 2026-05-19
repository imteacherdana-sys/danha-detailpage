# Image Production

Use this only after the user approves the full cut plan.

## Tool Rule

In Codex/ChatGPT, final images must be generated with the native image-generation tool. This workflow does not require the user to provide an OpenAI API key.

Do not claim that image generation is blocked because an API key is missing when the native image-generation tool is available.

Do not replace final image generation with:

- HTML/CSS screenshots.
- PIL/canvas-generated cards.
- Manual text overlays.
- Placeholder mockups.
- Cropped source photos with text pasted on top.

Those are not final ecommerce detail-page images. If the image-generation tool is unavailable, deliver only the approved cut plan and ask to continue in an environment where image generation is available.

## Parallel Production

Generate one image per cut:

- `section-01.png`
- `section-02.png`
- ...

Launch as many cut jobs in parallel as the environment supports. Each job owns only its assigned cut and output path.

## Final Image Requirements

Each image must be a finished mobile ecommerce detail-page cut:

- Approved Korean headline and subcopy rendered inside the image.
- Product photo or reference product appearance preserved.
- Mobile-readable typography.
- Strong contrast.
- No placeholder boxes, ASCII wireframes, blank text areas, or unlabeled mockup blocks.
- No unverified claims.

## Coupang Section 2 Prompt Requirements

The review cut prompt must specify:

- Soft review-bubble/card style similar to the approved sample.
- Exactly 5 review cards.
- Masked user ids.
- Four rectangular checkbox USP points under `우리 제품 이런분께 추천 드려요!`.
- Bottom CTA: `지금 바로 경험해보세요!`.
- Do not change, translate, or omit the Korean review text.

## QA

Fail and regenerate a cut if:

- Korean text is unreadable, broken, missing, or translated.
- Product color, label, package, or shape changed from reference photos.
- A review was invented or materially rewritten.
- Coupang cut order is broken.
- Product information disclosure is not the final cut.
- Any image is one merged long page instead of an individual cut.
