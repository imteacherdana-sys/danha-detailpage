"""
최종 상세페이지 기획서 HTML 렌더러 — 단아쌤 스킬

📦 단아쌤 개발 · 쇼핑몰스쿨 https://shoppingmallschool.com
   MIT License — 자유롭게 사용·수정·재배포 가능 (저작권 표기 유지)

plan.json (스킬이 작성한 섹션별 카피·이미지경로·태그)을 받아
클라이언트 전달 가능한 단일 HTML 파일을 만든다.

plan.json 스키마:
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
    "usps": ["1초 펼침", "10kg 견딤", "트렁크 슬림 수납", "방수 원단"]
  },
  "sections": [
    {
      "id": "hook",
      "name": "후킹 / 일상 불편 공감",
      "tags": ["AIDA-A", "PAS-P"],
      "ratio": "1:1",
      "slotType": "연출",
      "hook": "...",
      "body": "...",
      "imgPromptKo": "...",
      "imgPromptEn": "...",
      "imgPath": "output/section-01.png"
    }, ...
  ]
}

사용법:
  python render_html.py --plan plan.json --out 기획서.html
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import sys
from pathlib import Path


def img_to_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def render_section(idx: int, sec: dict, plan_dir: Path) -> str:
    img_path = sec.get("imgPath", "")
    img_uri = ""
    if img_path:
        p = Path(img_path)
        if not p.is_absolute():
            p = plan_dir / p
        img_uri = img_to_data_uri(p)

    img_html = (
        f'<img src="{img_uri}" alt="{html.escape(sec.get("name", ""))}">'
        if img_uri
        else '<div class="img-missing">이미지 미생성</div>'
    )
    body_html = html.escape(sec.get("body", "")).replace("\n", "<br>")

    return f"""
    <article class="section">
      <header class="section-head">
        <span class="num">{idx:02d}</span>
        <h2>{html.escape(sec.get("name", ""))}</h2>
        <span class="ratio">{html.escape(sec.get("ratio", ""))} · {html.escape(sec.get("slotType", ""))}</span>
      </header>
      <div class="grid">
        <div class="copy">
          <p class="hook">{html.escape(sec.get("hook", ""))}</p>
          <div class="body">{body_html}</div>
        </div>
        <div class="visual">{img_html}</div>
      </div>
      <details class="prompt">
        <summary>이미지 프롬프트</summary>
        <p><strong>🇰🇷</strong> {html.escape(sec.get("imgPromptKo", ""))}</p>
        <p><strong>🇺🇸</strong> {html.escape(sec.get("imgPromptEn", ""))}</p>
      </details>
    </article>
    """


HTML_SHELL = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: 'Pretendard', 'Apple SD Gothic Neo', system-ui, sans-serif; margin:0; background:#f7f5f2; color:#222; line-height:1.6; }}
  .wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px 24px 64px; }}
  header.hero {{ background: linear-gradient(135deg, #6c5ce7 0%, #fd79a8 100%); color:#fff; padding: 40px 32px; border-radius: 16px; margin-bottom: 32px; }}
  header.hero h1 {{ margin: 0 0 12px; font-size: 28px; }}
  header.hero .meta {{ opacity: 0.95; font-size: 14px; }}
  header.hero .meta span {{ margin-right: 16px; }}
  .section {{ background:#fff; border-radius: 14px; padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); }}
  .section-head {{ display:flex; align-items:center; gap:12px; margin-bottom: 16px; flex-wrap: wrap; }}
  .section-head .num {{ background:#6c5ce7; color:#fff; width:36px; height:36px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-weight:700; font-size:14px; }}
  .section-head h2 {{ margin:0; font-size: 20px; flex: 1 0 auto; }}
  .ratio {{ font-size: 12px; color:#888; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
  .copy .hook {{ font-size: 22px; font-weight: 700; margin: 0 0 14px; color:#2d2d2d; line-height: 1.35; }}
  .copy .body {{ font-size: 15px; color:#555; white-space: pre-line; }}
  .visual img {{ width:100%; height:auto; border-radius: 10px; display:block; }}
  .img-missing {{ background:#f5f5f5; border:2px dashed #ddd; padding: 40px 20px; text-align:center; color:#999; border-radius:10px; }}
  details.prompt {{ margin-top: 14px; padding: 12px; background: #fafafa; border-radius: 8px; font-size: 13px; color:#666; }}
  details.prompt summary {{ cursor: pointer; font-weight: 600; }}
  details.prompt p {{ margin: 6px 0; }}
  .toc {{ background:#fff; padding: 20px; border-radius: 12px; margin-bottom: 24px; }}
  .toc ol {{ margin: 0; padding-left: 24px; columns: 2; column-gap: 32px; }}
  .toc a {{ color: #6c5ce7; text-decoration: none; }}
  footer {{ text-align: center; color:#999; font-size: 13px; margin-top: 40px; }}
  @media (max-width: 720px) {{
    .grid {{ grid-template-columns: 1fr; }}
    .toc ol {{ columns: 1; }}
  }}
  @media print {{
    body {{ background: #fff; }}
    .section {{ box-shadow: none; page-break-inside: avoid; }}
  }}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <h1>{title}</h1>
    <div class="meta">
      <span><strong>카테고리</strong> {category}</span>
      <span><strong>보이스톤</strong> {voiceTone}</span>
      <span><strong>프레임워크</strong> {framework}</span>
      <span><strong>총 섹션</strong> {nSections}</span>
    </div>
    <div class="meta" style="margin-top:8px;">
      <span><strong>타겟</strong> {target}</span>
      <span><strong>가격</strong> {price}</span>
      <span><strong>옵션</strong> {variant}</span>
    </div>
  </header>

  <nav class="toc">
    <strong>섹션 목차</strong>
    <ol>{toc}</ol>
  </nav>

  {sections}

  <footer>단아쌤 한국형 상세페이지 스킬 · Claude Code + OpenAI gpt-image-1</footer>
</div>
</body>
</html>"""


def main() -> int:
    print("📦 단아쌤 한국형 상세페이지 스킬 · https://shoppingmallschool.com")
    ap = argparse.ArgumentParser(description="상세페이지 기획서 HTML 렌더링 (단아쌤 스킬)")
    ap.add_argument("--plan", required=True, help="plan.json 경로")
    ap.add_argument("--out", required=True, help="출력 HTML 경로")
    args = ap.parse_args()

    plan_path = Path(args.plan)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    meta = plan.get("meta", {})
    sections = plan.get("sections", [])

    plan_dir = plan_path.parent

    price = meta.get("productPrice", "")
    if price:
        try:
            price = f"{int(price):,}원"
        except (ValueError, TypeError):
            pass

    toc = "".join(
        f'<li><a href="#sec-{i}">{html.escape(s.get("name", ""))}</a></li>'
        for i, s in enumerate(sections, start=1)
    )
    sections_html = "".join(
        f'<a id="sec-{i}"></a>' + render_section(i, s, plan_dir)
        for i, s in enumerate(sections, start=1)
    )

    out_html = HTML_SHELL.format(
        title=html.escape(meta.get("productName", "상세페이지 기획서")),
        category=html.escape(meta.get("categoryName", "")),
        voiceTone=html.escape(meta.get("voiceToneName", "")),
        framework=html.escape((meta.get("framework", "") or "").upper()),
        nSections=len(sections),
        target=html.escape(meta.get("productTarget", "")),
        price=html.escape(price),
        variant=html.escape(meta.get("productVariant", "")),
        toc=toc,
        sections=sections_html,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out_html, encoding="utf-8")
    print(f"OK: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
