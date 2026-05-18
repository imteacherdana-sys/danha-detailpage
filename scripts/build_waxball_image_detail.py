from __future__ import annotations

import json
import shutil
import textwrap
import zipfile
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(
    r"C:\Users\atll\.codex\generated_images\019e39b6-84c2-7612-8f68-b1f3c49eb563"
    r"\ig_00b74a54682d5f93016a0ab16a589c8191b2fa6f618cb3ecae.png"
)
OUT_DIR = ROOT / "output" / "waxball_image_detail"
W, H = 860, 1200

FONT_BOLD = Path(r"C:\Windows\Fonts\GmarketSansTTFBold.ttf")
FONT_MED = Path(r"C:\Windows\Fonts\GmarketSansTTFMedium.ttf")
FONT_BODY = Path(r"C:\Windows\Fonts\NanumSquareNeo-cBd.ttf")


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw, xy, text, fnt, fill, stroke_width=0, stroke_fill=None):
    bbox = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=8, stroke_width=stroke_width)
    x = xy[0] - (bbox[2] - bbox[0]) / 2
    y = xy[1] - (bbox[3] - bbox[1]) / 2
    draw.multiline_text((x, y), text, font=fnt, fill=fill, spacing=8, align="center", stroke_width=stroke_width, stroke_fill=stroke_fill)


def wrap_ko(text: str, width: int) -> str:
    lines = []
    for raw in text.split("\n"):
        if len(raw) <= width:
            lines.append(raw)
        else:
            lines.extend(textwrap.wrap(raw, width=width, break_long_words=False, replace_whitespace=False))
    return "\n".join(lines)


def bg(color="#fff8e8") -> Image.Image:
    img = Image.new("RGB", (W, H), color)
    overlay = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((-180, -120, 300, 300), fill=(255, 142, 181, 42))
    od.ellipse((590, 70, 1010, 460), fill=(141, 231, 209, 50))
    od.ellipse((520, 760, 1040, 1320), fill=(158, 214, 240, 42))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def paste_fit(canvas: Image.Image, src: Image.Image, box, crop=None, radius=24):
    target_w = box[2] - box[0]
    target_h = box[3] - box[1]
    work = src.crop(crop) if crop else src.copy()
    work = ImageOps_fit(work, (target_w, target_h))
    mask = Image.new("L", (target_w, target_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, target_w, target_h), radius=radius, fill=255)
    canvas.paste(work.convert("RGBA"), (box[0], box[1]), mask)


def ImageOps_fit(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    sw, sh = img.size
    tw, th = size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    resized = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def draw_header(draw, title, subtitle=None, y=86, color="#3f3f46"):
    center_text(draw, (W // 2, y), title, font(FONT_BOLD, 56), color, stroke_width=3, stroke_fill="#ffffff")
    if subtitle:
        center_text(draw, (W // 2, y + 84), subtitle, font(FONT_BODY, 28), "#66666d")


def pill(draw, text, xy, fill="#ffffff", ink="#4b4b52", outline="#ece2d8"):
    f = font(FONT_BOLD, 25)
    bbox = draw.textbbox((0, 0), text, font=f)
    pad_x, pad_y = 24, 13
    x, y = xy
    rounded(draw, (x, y, x + bbox[2] + pad_x * 2, y + bbox[3] + pad_y * 2), 30, fill, outline, 2)
    draw.text((x + pad_x, y + pad_y - 2), text, font=f, fill=ink)


def section_01(src):
    im = bg()
    d = ImageDraw.Draw(im)
    draw_header(d, "왁뿌볼\n왁스말랑이", "누르면 말랑, 손끝엔 바작바작", y=140, color="#ee6f9e")
    paste_fit(im, src, (42, 340, 818, 1080), crop=(0, 520, src.width, src.height), radius=30)
    pill(d, "SNS 대란템!", (270, 1010), fill="#ff7fa8", ink="#ffffff", outline="#ff7fa8")
    return im


def section_02(src):
    im = bg("#f6fbf7")
    d = ImageDraw.Draw(im)
    draw_header(d, "손이 심심한 순간 있죠?", "공부할 때 · 일할 때 · 영상 볼 때", y=120)
    paste_fit(im, src, (95, 290, 765, 820), crop=(0, 760, src.width, src.height), radius=34)
    center_text(d, (W // 2, 930), "괜히 손끝이 허전한 순간\n꾹 눌렀다 놓는 말랑한 재미!", font(FONT_BOLD, 38), "#4c4c52")
    pill(d, "손심심 해결!", (292, 1038), fill="#8de7d1")
    return im


def section_03(src):
    im = bg("#f8f2ff")
    d = ImageDraw.Draw(im)
    draw_header(d, "말랑한데, 바작해요", "겉은 투명하고 탱글 · 속은 크랙 비주얼", y=120)
    paste_fit(im, src, (48, 290, 812, 820), crop=(0, 470, src.width, 1320), radius=30)
    for x, txt in [(96, "투명 외피"), (330, "크랙 질감"), (568, "말랑 압착")]:
        rounded(d, (x, 890, x + 196, 1012), 24, "#ffffff", "#eadff8", 2)
        center_text(d, (x + 98, 951), txt, font(FONT_BOLD, 27), "#5c5370")
    center_text(d, (W // 2, 1082), "누를수록 달라지는 모양까지 재미있게", font(FONT_BODY, 30), "#66666d")
    return im


def section_04(src):
    im = bg("#fff4f8")
    d = ImageDraw.Draw(im)
    draw_header(d, "취향 따라 고르는 5컬러", "컬러마다 다른 무드로 골라보세요", y=116, color="#f0719e")
    paste_fit(im, src, (55, 255, 805, 765), crop=(0, 470, src.width, 1050), radius=30)
    colors = [("ML1", "무지개", "#ffe27a"), ("ML2", "두픈쿠", "#6d2d3b"), ("ML3", "민트초코", "#8de7d1"), ("ML4", "화이트핑크", "#ffb5cf"), ("ML5", "블루핑크", "#9ed6f0")]
    x0 = 80
    for i, (code, name, col) in enumerate(colors):
        x = x0 + i * 142
        d.ellipse((x, 840, x + 90, 930), fill=col, outline="#ffffff", width=6)
        center_text(d, (x + 45, 985), f"{code}\n{name}", font(FONT_BOLD, 22), "#4c4c52")
    return im


def section_05(src):
    im = bg("#f3fbff")
    d = ImageDraw.Draw(im)
    draw_header(d, "책상 위 작은 기분전환", "오늘의 데스크 위에 말랑함 한 스푼", y=116, color="#559cc0")
    paste_fit(im, src, (66, 280, 794, 840), crop=(0, 650, src.width, src.height), radius=32)
    center_text(d, (W // 2, 950), "공부하다가 한 번 꾹\n업무 중에도 한 번 말랑", font(FONT_BOLD, 40), "#45454b")
    pill(d, "기분전환템", (300, 1050), fill="#9ed6f0")
    return im


def section_06(src):
    im = bg("#fff8ef")
    d = ImageDraw.Draw(im)
    draw_header(d, "한 손에 쏙", "제품 사이즈 약 5.5 x 5.5cm", y=116, color="#6a2934")
    paste_fit(im, src, (145, 295, 715, 865), crop=(0, 850, src.width, src.height), radius=38)
    d.line((220, 930, 640, 930), fill="#6a2934", width=5)
    d.polygon([(220, 930), (245, 915), (245, 945)], fill="#6a2934")
    d.polygon([(640, 930), (615, 915), (615, 945)], fill="#6a2934")
    center_text(d, (W // 2, 1000), "5.5 x 5.5cm", font(FONT_BOLD, 46), "#6a2934")
    center_text(d, (W // 2, 1082), "책상 위, 파우치 속에 두기 좋은 둥근 크기", font(FONT_BODY, 28), "#68686f")
    return im


def section_07(src):
    im = bg("#f7fff9")
    d = ImageDraw.Draw(im)
    draw_header(d, "더 탱글하게 즐기는 팁", "사용 전 60분 냉장 보관 권장", y=116, color="#3d9f82")
    paste_fit(im, src, (110, 300, 750, 820), crop=(420, 520, src.width, 1250), radius=32)
    rounded(d, (145, 880, 715, 1040), 28, "#ffffff", "#cfeee2", 3)
    center_text(d, (W // 2, 940), "온도에 따라 제형이 달라질 수 있어요", font(FONT_BODY, 29), "#5f6663")
    center_text(d, (W // 2, 1000), "60분 냉장 후 사용하면 더 탱글하게", font(FONT_BOLD, 32), "#3d9f82")
    return im


def section_08(src):
    im = bg("#fff4fb")
    d = ImageDraw.Draw(im)
    draw_header(d, "귀엽게 보관하고 선물하기", "투명 캡슐 느낌의 말랑이 무드", y=116, color="#e86999")
    paste_fit(im, src, (55, 280, 805, 835), crop=(0, 430, src.width, 980), radius=34)
    center_text(d, (W // 2, 942), "동그란 비주얼 그대로\n보는 재미까지 챙긴 감성템", font(FONT_BOLD, 38), "#4c4c52")
    pill(d, "선물용으로도 귀엽게", (238, 1050), fill="#ffffff", ink="#e86999")
    return im


def section_09(src):
    im = bg("#f9f9f9")
    d = ImageDraw.Draw(im)
    draw_header(d, "구매 전 꼭 확인해주세요", "안전하게 즐기기 위한 사용 안내", y=106)
    items = [
        ("14세 이상 사용 권장", "어린이가 입에 넣지 않도록 주의해주세요."),
        ("먹는 용도 금지", "입에 넣거나 먹는 등 용도 외 사용은 피해주세요."),
        ("먼지 부착 가능", "재질 특성상 표면에 먼지가 붙을 수 있습니다."),
        ("60분 냉장 권장", "온도에 따라 제형이 달라질 수 있습니다."),
    ]
    y = 260
    for title, body in items:
        rounded(d, (70, y, 790, y + 138), 26, "#ffffff", "#e6e6e6", 2)
        d.ellipse((100, y + 42, 154, y + 96), fill="#ff8eb5")
        center_text(d, (127, y + 69), "!", font(FONT_BOLD, 34), "#ffffff")
        d.text((180, y + 30), title, font=font(FONT_BOLD, 30), fill="#44444a")
        d.text((180, y + 78), body, font=font(FONT_BODY, 23), fill="#6b6b72")
        y += 160
    paste_fit(im, src, (252, 910, 608, 1130), crop=(0, 700, src.width, src.height), radius=28)
    return im


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    src = Image.open(SOURCE).convert("RGB")
    shutil.copy2(SOURCE, OUT_DIR / "ai_generated_source.png")
    makers = [section_01, section_02, section_03, section_04, section_05, section_06, section_07, section_08, section_09]
    paths = []
    for idx, make in enumerate(makers, start=1):
        im = make(src).convert("RGB")
        path = OUT_DIR / f"section-{idx:02d}.png"
        im.save(path, quality=95)
        paths.append(path)

    full = Image.new("RGB", (W, H * len(paths)), "#fff8e8")
    for idx, path in enumerate(paths):
        full.paste(Image.open(path).convert("RGB"), (0, H * idx))
    full_path = OUT_DIR / "왁뿌볼_상세페이지_전체.png"
    full.save(full_path, quality=95)

    plan = {
        "productName": "왁뿌볼 왁스말랑이",
        "format": "PNG image detail page",
        "sourcePolicy": "Original AI-generated product visual only. Competitor images were not used in final assets.",
        "createdAt": datetime.now().isoformat(timespec="seconds"),
        "sections": [path.name for path in paths],
        "fullPage": full_path.name,
        "removedFromFinal": ["AIDA/PAS/internal planning labels", "competitor product images", "unverified certification claims"],
        "compliance": ["14세 이상 사용 권장", "먹는 용도 금지", "먼지 부착 가능", "60분 냉장 권장"],
    }
    (OUT_DIR / "plan_image_detail.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    zip_path = OUT_DIR / "왁뿌볼_이미지형_상세페이지.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in paths:
            zf.write(path, path.name)
        zf.write(full_path, full_path.name)
        zf.write(OUT_DIR / "plan_image_detail.json", "plan_image_detail.json")
    print(OUT_DIR)


if __name__ == "__main__":
    main()
