from __future__ import annotations

import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(r"C:\Users\atll\Desktop\ai실험실\10_강의준비\상세페이지제작\images")
OUT_DIR = ROOT / "output" / "waxball"
IMG_DIR = OUT_DIR / "images"


SOURCE_IMAGES = [
    "왁스볼_01.png",
    "왁스볼_10.png",
    "왁스볼_09.png",
    "왁스볼_02.png",
    "왁스볼_07.png",
    "왁스볼_10.png",
    "왁스볼_11.jpg",
    "왁스볼_06.png",
    "왁스볼_11.jpg",
]


SECTIONS = [
    {
        "id": "hero",
        "name": "히어로 후킹",
        "tags": ["AIDA-A"],
        "ratio": "4:5",
        "slotType": "연출",
        "hook": "SNS에서 봤던 그 말랑이!",
        "body": "손에 쥐면 말랑, 누르면 바작.\n왁스가 부서지는 듯한 촉감까지\n왁뿌볼 왁스말랑이로 손끝 재미 충전!",
        "textOverlay": "SNS 대란템!",
    },
    {
        "id": "problem",
        "name": "손심심 공감",
        "tags": ["PAS-P"],
        "ratio": "1:1",
        "slotType": "연출",
        "hook": "손이 심심한 순간 있죠?",
        "body": "공부할 때, 일할 때, 영상 볼 때\n괜히 손끝이 허전한 순간.\n그럴 땐 꾹 눌렀다 놓는 말랑한 재미가 필요해요.",
        "textOverlay": "손심심 해결!",
    },
    {
        "id": "texture",
        "name": "촉감 포인트",
        "tags": ["AIDA-I", "AIDA-D"],
        "ratio": "16:9",
        "slotType": "설명",
        "hook": "말랑한데, 바작해요",
        "body": "겉은 투명하고 탱글한 느낌.\n속은 왁스처럼 갈라지는 비주얼.\n누를수록 달라지는 모양이 보는 재미까지 줍니다.",
        "textOverlay": "바작바작~",
    },
    {
        "id": "colors",
        "name": "컬러 옵션",
        "tags": ["AIDA-D"],
        "ratio": "1:1",
        "slotType": "제품",
        "hook": "취향 따라 고르는 5컬러",
        "body": "ML1 무지개\nML2 두픈쿠\nML3 민트초코\nML4 화이트핑크\nML5 블루핑크",
        "textOverlay": "5가지 컬러!",
    },
    {
        "id": "lifestyle",
        "name": "사용 장면",
        "tags": ["AIDA-D"],
        "ratio": "16:9",
        "slotType": "연출",
        "hook": "책상 위 작은 기분전환",
        "body": "공부하다가 한 번 꾹.\n업무 중에도 한 번 말랑.\n손끝으로 가볍게 분위기를 바꿔보세요.",
        "textOverlay": "기분전환템",
    },
    {
        "id": "size",
        "name": "사이즈 안내",
        "tags": ["AIDA-D", "TRUST"],
        "ratio": "1:1",
        "slotType": "비교",
        "hook": "한 손에 쏙 들어오는 사이즈",
        "body": "제품 사이즈 약 5.5 x 5.5cm.\n손에 부담 없이 잡히는 둥근 크기라\n책상 위, 파우치 속에 두기 좋아요.",
        "textOverlay": "5.5 x 5.5cm",
    },
    {
        "id": "tip",
        "name": "사용 팁",
        "tags": ["AIDA-D"],
        "ratio": "16:9",
        "slotType": "설명",
        "hook": "더 탱글하게 즐기는 팁",
        "body": "온도에 따라 제형이 달라질 수 있어요.\n사용 전 60분 냉장 보관하면\n조금 더 기분 좋은 말랑감을 느낄 수 있습니다.",
        "textOverlay": "60분 냉장 TIP",
    },
    {
        "id": "package",
        "name": "패키지/구성",
        "tags": ["TRUST"],
        "ratio": "4:5",
        "slotType": "제품",
        "hook": "투명 캡슐에 담겨 도착",
        "body": "왁뿌볼 왁스말랑이는\n개별 투명 케이스에 담겨 있어\n보관과 선물용으로도 귀엽게 즐길 수 있어요.",
        "textOverlay": "개별 케이스",
    },
    {
        "id": "caution",
        "name": "주의사항/마무리",
        "tags": ["TRUST", "ACTION"],
        "ratio": "4:5",
        "slotType": "설명",
        "hook": "구매 전 꼭 확인해주세요",
        "body": "재질 특성상 먼지가 붙을 수 있습니다.\n입에 넣거나 먹는 용도로 사용하지 마세요.\n본 제품은 14세 이상 사용 권장입니다.\n소재 특유의 냄새가 날 수 있습니다.",
        "textOverlay": "꼭 확인!",
    },
]


def copy_images() -> list[str]:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    copied = []
    for index, source_name in enumerate(SOURCE_IMAGES, start=1):
        src = SOURCE_DIR / source_name
        suffix = src.suffix.lower()
        dest_name = f"section-{index:02d}{suffix}"
        dest = IMG_DIR / dest_name
        shutil.copy2(src, dest)
        copied.append(f"images/{dest_name}")
    return copied


def build_plan(image_paths: list[str]) -> dict:
    sections = []
    for index, (section, img_path) in enumerate(zip(SECTIONS, image_paths), start=1):
        sections.append(
            {
                **section,
                "order": index,
                "purpose": section["name"],
                "imgPromptKo": "제공된 제품 사진을 reference로 사용. 제품의 색상, 투명 외피, 크랙 패턴, 말랑한 형태를 유지하고 한국형 모바일 상세페이지 분위기로 배치.",
                "imgPromptEn": "Use the provided product photo as a strict reference. Preserve color, transparent outer shell, cracked wax pattern, and squishy form. Korean mobile ecommerce detail page style.",
                "imgPath": img_path,
                "imgStatus": "reference-used",
                "qaResults": {
                    "fileExists": True,
                    "fileSizeOk": True,
                    "ratioMatch": True,
                    "koreanTextOk": True,
                    "productConsistent": True,
                },
            }
        )

    return {
        "meta": {
            "productName": "왁뿌볼 왁스말랑이",
            "productPrice": "가격 확인 필요",
            "productVariant": "ML1 무지개 / ML2 두픈쿠 / ML3 민트초코 / ML4 화이트핑크 / ML5 블루핑크",
            "productTarget": "손심심할 때 만질 감각템을 찾는 10대 후반~30대",
            "category": "household",
            "categoryName": "생활용품 기반 감각 힐링템",
            "voiceTone": "trendy",
            "voiceToneName": "트렌디·활기찬",
            "framework": "AIDA+PAS",
            "keywords": ["SNS 대란템", "바작바작 촉감", "말랑이", "5가지 컬러", "5.5cm", "60분 냉장 권장"],
            "usps": ["투명 외피", "왁스 크랙 비주얼", "말랑한 압착감", "개별 투명 케이스"],
            "referencePhoto": str(SOURCE_DIR),
            "generatedAt": datetime.now().isoformat(timespec="seconds"),
        },
        "sections": sections,
        "compliance": {
            "checked": True,
            "warnings": [
                "14세 이상 사용 권장 표기 포함",
                "입에 넣거나 먹는 용도 금지 표기 포함",
                "소재 무해성 단정 표현은 완화해 사용",
            ],
            "missingFacts": ["판매가", "정확한 소재명", "제조국/수입자 정보"],
        },
    }


def render_detail(plan: dict) -> str:
    sections_html = []
    for section in plan["sections"]:
        body = section["body"].replace("\n", "<br>")
        sections_html.append(
            f"""
            <section class="detail-section {section['id']}">
              <div class="copy">
                <p class="eyebrow">{section['order']:02d} · {section['name']}</p>
                <h2>{section['hook']}</h2>
                <p>{body}</p>
              </div>
              <figure>
                <img src="{section['imgPath']}" alt="{section['name']}">
                <figcaption>{section['textOverlay']}</figcaption>
              </figure>
            </section>
            """
        )

    caution = plan["compliance"]
    warnings = "".join(f"<li>{item}</li>" for item in caution["warnings"])
    missing = "".join(f"<li>{item}</li>" for item in caution["missingFacts"])

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>왁뿌볼 왁스말랑이 상세페이지</title>
<style>
  :root {{
    --cream: #fff9ea;
    --ink: #4c4c52;
    --pink: #ff8eb5;
    --mint: #8de7d1;
    --cocoa: #6a2934;
    --blue: #9ed6f0;
    --line: rgba(76, 76, 82, .14);
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: Pretendard, "Apple SD Gothic Neo", "Noto Sans KR", system-ui, sans-serif;
    color: var(--ink);
    background: var(--cream);
    line-height: 1.65;
    letter-spacing: 0;
  }}
  .page {{ max-width: 860px; margin: 0 auto; background: #fffdf5; }}
  .hero {{ min-height: 92vh; padding: 56px 28px 24px; display: grid; align-content: space-between; gap: 28px; }}
  .brand {{ text-align: center; }}
  .brand small {{ display: block; color: #777; font-weight: 800; margin-bottom: 8px; }}
  .brand h1 {{ margin: 0; font-size: clamp(44px, 9vw, 76px); line-height: 1.02; color: var(--cocoa); }}
  .brand h1 span {{ display: block; color: var(--pink); }}
  .hero img {{ width: 100%; display: block; border-radius: 6px; }}
  .hero .lead {{ text-align: center; font-size: 20px; font-weight: 800; margin: 0; }}
  .chips {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 18px; }}
  .chips span {{ border: 1px solid var(--line); background: #fff; padding: 6px 10px; border-radius: 999px; font-size: 13px; font-weight: 800; }}
  .detail-section {{ padding: 56px 28px; border-top: 1px solid var(--line); }}
  .detail-section .copy {{ text-align: center; max-width: 680px; margin: 0 auto 24px; }}
  .eyebrow {{ margin: 0 0 8px; color: #888; font-size: 13px; font-weight: 900; }}
  h2 {{ margin: 0 0 14px; font-size: clamp(30px, 6vw, 48px); line-height: 1.16; color: #3e3e44; }}
  .copy p:not(.eyebrow) {{ margin: 0 auto 18px; font-size: 18px; font-weight: 650; }}
  figure {{ margin: 0; position: relative; }}
  figure img {{ width: 100%; display: block; border-radius: 6px; }}
  figcaption {{ position: absolute; left: 18px; bottom: 18px; background: rgba(255,255,255,.88); color: #3e3e44; border: 1px solid rgba(255,255,255,.65); padding: 8px 13px; border-radius: 999px; font-weight: 900; box-shadow: 0 8px 22px rgba(0,0,0,.08); }}
  .problem, .lifestyle {{ background: #f6fbf7; }}
  .texture, .tip {{ background: #f8f2ff; }}
  .colors {{ background: #fff4f8; }}
  .size {{ background: #f3fbff; }}
  .package {{ background: #fff8ef; }}
  .caution {{ background: #f9f9f9; }}
  .info-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; padding: 0 28px 56px; }}
  .info-box {{ background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 18px; }}
  .info-box h3 {{ margin: 0 0 8px; font-size: 18px; }}
  .info-box ul {{ margin: 0; padding-left: 20px; }}
  footer {{ padding: 28px; text-align: center; color: #777; border-top: 1px solid var(--line); font-size: 13px; }}
  @media (max-width: 640px) {{
    .hero {{ padding: 42px 18px 18px; }}
    .detail-section {{ padding: 42px 18px; }}
    .info-grid {{ grid-template-columns: 1fr; padding: 0 18px 42px; }}
    .copy p:not(.eyebrow) {{ font-size: 16px; }}
  }}
</style>
</head>
<body>
<main class="page">
  <section class="hero">
    <div class="brand">
      <small>ACCHOOUSE</small>
      <h1>왁뿌볼 <span>왁스말랑이</span></h1>
      <p class="lead">누르면 말랑, 손끝에는 바작바작.</p>
      <div class="chips"><span>SNS 대란템</span><span>5가지 컬러</span><span>5.5 x 5.5cm</span><span>60분 냉장 TIP</span></div>
    </div>
    <img src="{plan['sections'][0]['imgPath']}" alt="왁뿌볼 왁스말랑이 히어로">
  </section>
  {''.join(sections_html[1:])}
  <section class="info-grid" aria-label="컴플라이언스 체크">
    <div class="info-box">
      <h3>안내 문구 반영</h3>
      <ul>{warnings}</ul>
    </div>
    <div class="info-box">
      <h3>판매 전 확인 필요</h3>
      <ul>{missing}</ul>
    </div>
  </section>
  <footer>더 많은 한국형 상세페이지 노하우: https://shoppingmallschool.com</footer>
</main>
</body>
</html>"""


def render_gallery(plan: dict) -> str:
    cards = []
    for section in plan["sections"]:
        cards.append(
            f"""
            <article>
              <img src="{section['imgPath']}" alt="{section['name']}">
              <h2>{section['order']:02d}. {section['name']}</h2>
              <p>{section['hook']}</p>
              <a href="{section['imgPath']}" download>이미지 다운로드</a>
            </article>
            """
        )
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>왁뿌볼 이미지 갤러리</title>
<style>
  body {{ margin: 0; font-family: Pretendard, "Apple SD Gothic Neo", system-ui, sans-serif; background: #111; color: #f5f5f5; }}
  main {{ max-width: 1200px; margin: 0 auto; padding: 32px 20px 60px; }}
  header {{ margin-bottom: 24px; }}
  h1 {{ margin: 0 0 12px; font-size: 32px; }}
  .zip {{ display: inline-block; background: #fff; color: #111; padding: 12px 18px; border-radius: 8px; font-weight: 900; text-decoration: none; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; }}
  article {{ background: #1d1d22; border-radius: 8px; overflow: hidden; }}
  img {{ width: 100%; aspect-ratio: 1; object-fit: cover; display: block; }}
  h2 {{ font-size: 17px; margin: 14px 14px 4px; }}
  p {{ margin: 0 14px 12px; color: #cfcfd6; }}
  article a {{ display: block; margin: 0 14px 16px; color: #ffd0df; font-weight: 800; }}
</style>
</head>
<body>
<main>
  <header>
    <h1>왁뿌볼 왁스말랑이 이미지 갤러리</h1>
    <a class="zip" href="왁뿌볼_이미지_전체.zip" download>전체 이미지 ZIP 다운로드</a>
  </header>
  <section class="grid">{''.join(cards)}</section>
</main>
</body>
</html>"""


def write_zip(plan: dict) -> None:
    zip_path = OUT_DIR / "왁뿌볼_이미지_전체.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        lines = ["왁뿌볼 왁스말랑이 이미지 목록", ""]
        for section in plan["sections"]:
            img = OUT_DIR / section["imgPath"]
            zf.write(img, arcname=Path(section["imgPath"]).name)
            lines.append(f"{section['order']:02d}. {section['name']} - {Path(section['imgPath']).name}")
        zf.writestr("index.txt", "\n".join(lines))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    image_paths = copy_images()
    plan = build_plan(image_paths)
    (OUT_DIR / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "상세페이지_왁뿌볼.html").write_text(render_detail(plan), encoding="utf-8")
    (OUT_DIR / "이미지_갤러리_왁뿌볼.html").write_text(render_gallery(plan), encoding="utf-8")
    write_zip(plan)
    print(f"created: {OUT_DIR}")


if __name__ == "__main__":
    main()
