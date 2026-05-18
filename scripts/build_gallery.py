"""
이미지 갤러리 + 전체 다운로드 ZIP 빌더 — 단아쌤 상세페이지 스킬

📦 단아쌤 개발 · 쇼핑몰스쿨 https://shoppingmallschool.com
   MIT License — 자유롭게 사용·수정·재배포 가능 (저작권 표기 유지)

plan.json + 생성된 PNG 파일들을 받아서:
1. 갤러리 HTML 생성 (썸네일 그리드 + 컷별 다운로드 + QA 상태)
2. 전체 이미지를 ZIP으로 묶음 (이미지_전체.zip)
3. HTML의 '전체 다운로드' 버튼이 ZIP을 가리키도록 자동 링크

API 불필요 — 로컬 파일 처리만.

사용법:
  python build_gallery.py --plan output/plan.json --images-dir output --out output/이미지_갤러리.html
"""

from __future__ import annotations

import argparse
import html
import json
import sys
import zipfile
from pathlib import Path


def collect_image_files(plan: dict, images_dir: Path) -> list[dict]:
    """plan의 sections 순서대로 이미지 파일 정보를 모은다."""
    items = []
    for sec in plan.get("sections", []):
        rel_path = sec.get("imgPath", "")
        if not rel_path:
            items.append({**sec, "_resolved_path": None, "_exists": False, "_size": 0})
            continue
        p = Path(rel_path)
        if not p.is_absolute():
            p = images_dir / p.name if not (images_dir / rel_path).exists() else images_dir / rel_path
        exists = p.exists()
        size = p.stat().st_size if exists else 0
        items.append({**sec, "_resolved_path": p, "_exists": exists, "_size": size})
    return items


def build_zip(items: list[dict], out_zip: Path) -> int:
    """존재하는 이미지를 ZIP으로 묶고 index.txt를 함께 포함."""
    count = 0
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        index_lines = ["단아쌤 한국형 상세페이지 스킬 — 이미지 목록", "https://shoppingmallschool.com", ""]
        for i, item in enumerate(items, start=1):
            if not item["_exists"]:
                continue
            arcname = f"section-{i:02d}.png"
            zf.write(item["_resolved_path"], arcname=arcname)
            index_lines.append(f"{arcname}  —  {item.get('name', '')}  ({item.get('ratio', '')})")
            count += 1
        zf.writestr("index.txt", "\n".join(index_lines).encode("utf-8"))
    return count


def render_status_badge(item: dict) -> str:
    if not item.get("_exists"):
        return '<span class="badge badge-fail">❌ 미생성</span>'
    qa = item.get("qaResults", {})
    if qa:
        failed = [k for k, v in qa.items() if v is False]
        if failed:
            return f'<span class="badge badge-warn">⚠️ QA 부분 통과</span>'
        return '<span class="badge badge-ok">✅ QA 통과</span>'
    if item["_size"] < 50_000:
        return '<span class="badge badge-warn">⚠️ 파일 작음</span>'
    return '<span class="badge badge-ok">✅ 생성됨</span>'


def render_card(idx: int, item: dict, images_dir: Path, out_dir: Path) -> str:
    name = html.escape(item.get("name", f"섹션 {idx}"))
    ratio = html.escape(item.get("ratio", ""))
    slot = html.escape(item.get("slotType", ""))
    status = render_status_badge(item)

    if item["_exists"]:
        # 갤러리 HTML과 이미지가 같은 폴더에 있다고 가정 → 상대경로
        try:
            rel = item["_resolved_path"].relative_to(out_dir)
        except ValueError:
            rel = item["_resolved_path"].name
        img_src = str(rel).replace("\\", "/")
        img_html = (
            f'<a href="{img_src}" target="_blank">'
            f'<img src="{img_src}" alt="{name}" loading="lazy"></a>'
        )
        download_btn = f'<a class="btn btn-sm" href="{img_src}" download>📥 다운로드</a>'
    else:
        img_html = '<div class="img-missing">이미지 미생성</div>'
        download_btn = ''

    return f"""
    <article class="card">
      <header>
        <span class="num">{idx:02d}</span>
        <h3>{name}</h3>
        {status}
      </header>
      <div class="visual">{img_html}</div>
      <div class="meta">
        <span class="ratio">{ratio} · {slot}</span>
      </div>
      <footer>{download_btn}</footer>
    </article>
    """


HTML_SHELL = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>이미지 갤러리 — {title}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Pretendard', 'Apple SD Gothic Neo', system-ui, sans-serif; margin:0; background:#0e0e10; color:#e8e8ec; line-height:1.55; }}
  .wrap {{ max-width: 1400px; margin: 0 auto; padding: 32px 24px 64px; }}
  header.hero {{ background: linear-gradient(135deg, #6c5ce7 0%, #fd79a8 100%); padding: 32px 28px; border-radius: 16px; margin-bottom: 28px; color:#fff; }}
  header.hero h1 {{ margin: 0 0 8px; font-size: 26px; }}
  header.hero .sub {{ opacity: 0.9; font-size: 14px; margin-bottom: 16px; }}
  .btn {{ display:inline-block; background:#fff; color:#6c5ce7; padding: 10px 18px; border-radius:8px; text-decoration:none; font-weight:700; font-size:14px; transition: transform 0.1s; }}
  .btn:hover {{ transform: translateY(-2px); }}
  .btn-big {{ padding: 14px 24px; font-size: 16px; }}
  .btn-sm {{ font-size:12px; padding:6px 12px; background:#2a2a30; color:#e8e8ec; }}
  .stats {{ display:flex; gap: 24px; margin-top: 16px; font-size: 13px; opacity: 0.9; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }}
  .card {{ background:#16161a; border-radius: 12px; padding: 16px; transition: transform 0.15s, box-shadow 0.15s; }}
  .card:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(108, 92, 231, 0.2); }}
  .card header {{ display:flex; align-items:center; gap:8px; margin-bottom: 12px; }}
  .card .num {{ background:#6c5ce7; color:#fff; width:28px; height:28px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-weight:700; font-size:12px; flex-shrink: 0; }}
  .card h3 {{ margin:0; font-size: 14px; flex: 1; color:#e8e8ec; }}
  .visual {{ background:#0a0a0c; border-radius: 8px; overflow:hidden; aspect-ratio: 1; margin-bottom: 10px; }}
  .visual img {{ width:100%; height:100%; object-fit: cover; display:block; }}
  .img-missing {{ display:flex; align-items:center; justify-content:center; height:100%; color:#666; font-size:12px; }}
  .meta {{ display:flex; flex-wrap:wrap; gap:8px; margin-bottom: 12px; font-size: 11px; }}
  .ratio {{ color:#888; }}
  .badge {{ font-size: 11px; padding: 3px 8px; border-radius: 10px; white-space: nowrap; }}
  .badge-ok {{ background:#1f3a2e; color: #4ade80; }}
  .badge-warn {{ background:#3a2f1f; color: #fbbf24; }}
  .badge-fail {{ background:#3a1f1f; color: #f87171; }}
  .card footer {{ display:flex; justify-content:flex-end; }}
  footer.site {{ text-align: center; color:#666; font-size: 12px; margin-top: 48px; padding-top: 24px; border-top: 1px solid #2a2a30; }}
  footer.site a {{ color:#a78bfa; text-decoration: none; }}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <h1>🎨 {title} — 이미지 갤러리</h1>
    <div class="sub">단아쌤 한국형 상세페이지 스킬로 생성된 {total_count}장의 이미지</div>
    <a class="btn btn-big" href="{zip_name}" download>📦 전체 다운로드 (ZIP, {zip_size_kb}KB)</a>
    <div class="stats">
      <span>✅ 생성: {ok_count} / {total_count}</span>
      <span>📐 비율: {ratios}</span>
      <span>🎭 보이스톤: {voice_tone}</span>
    </div>
  </header>

  <div class="grid">{cards}</div>

  <footer class="site">
    더 많은 한국형 상세페이지 노하우 · <a href="https://shoppingmallschool.com">쇼핑몰스쿨</a> · 단아쌤 개발 · MIT License
  </footer>
</div>
</body>
</html>"""


def main() -> int:
    print("📦 단아쌤 한국형 상세페이지 스킬 · https://shoppingmallschool.com")
    ap = argparse.ArgumentParser(description="이미지 갤러리 + 전체 ZIP 빌더 (단아쌤 스킬)")
    ap.add_argument("--plan", required=True, help="plan.json 경로")
    ap.add_argument("--images-dir", required=True, help="PNG 파일들이 있는 폴더")
    ap.add_argument("--out", required=True, help="출력 HTML 경로")
    ap.add_argument("--zip-name", default="이미지_전체.zip", help="ZIP 파일명 (HTML과 같은 폴더)")
    args = ap.parse_args()

    plan_path = Path(args.plan)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    meta = plan.get("meta", {})

    images_dir = Path(args.images_dir)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_dir = out_path.parent

    items = collect_image_files(plan, images_dir)
    total = len(items)
    ok = sum(1 for it in items if it["_exists"])

    # ZIP 생성
    zip_path = out_dir / args.zip_name
    zip_count = build_zip(items, zip_path)
    zip_kb = zip_path.stat().st_size // 1024 if zip_path.exists() else 0

    # 카드 렌더링
    cards_html = "".join(render_card(i, it, images_dir, out_dir) for i, it in enumerate(items, start=1))

    # 비율 통계
    ratios = sorted(set(it.get("ratio", "") for it in items if it.get("ratio")))

    out_html = HTML_SHELL.format(
        title=html.escape(meta.get("productName", "상세페이지")),
        total_count=total,
        ok_count=ok,
        zip_name=html.escape(args.zip_name),
        zip_size_kb=zip_kb,
        ratios=", ".join(ratios),
        voice_tone=html.escape(meta.get("voiceToneName", "")),
        cards=cards_html,
    )

    out_path.write_text(out_html, encoding="utf-8")
    print(f"OK: 갤러리 HTML → {out_path}")
    print(f"OK: 전체 ZIP → {zip_path} ({zip_count}장, {zip_kb}KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
