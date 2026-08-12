#!/usr/bin/env python3
"""
Watermark apply tool — Horizon Team standard (per Alan 2026-08-12)
- 文字 Horizon.Team
- 字體 LiberationSans-Bold.ttf 14pt × 2 = 28pt
- 顏色 白色 (255,255,255)
- Opacity 30%
- 3 柱位置 5% / 50% / 95%
- 縱向間距 text_h × 8.0
- 整體傾斜 -30° (逆時針)
- 模糊半徑 0.5 × scale (低模糊)
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
TEXT = "Horizon.Team"
FONT_SIZE_PT = 28          # 14pt × 2
OPACITY = int(255 * 0.30)  # 30%
COLS_X = [0.05, 0.50, 0.95]
ROW_SPACING = 8.0           # text_h × 8.0
ANGLE = -30                 # 逆時針
BLUR_SCALE = 0.5           # 模糊半徑 = 0.5 × scale

def apply_watermark(src_path: str, dst_path: str, target_long_edge: int = 1024) -> None:
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    scale = max(w, h) / target_long_edge

    # Font setup (28pt at base; PIL needs px for normal screens; using 28 directly works for ~72dpi)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE_PT)
    bbox = font.getbbox(TEXT)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    row_step = int(text_h * ROW_SPACING)

    # Build overlay canvas at 2x for blur, then downsample
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Generate tilted text on a transparent tile, then paste at column x-positions
    tile_w = int(text_w * 1.4)
    tile_h = int(text_h * 1.4)
    tile = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.text((-bbox[0], -bbox[1]), TEXT, font=font, fill=(255, 255, 255, OPACITY))
    tile = tile.rotate(ANGLE, resample=Image.BICUBIC, expand=True)

    # Columns
    for col in COLS_X:
        x = int(w * col) - tile.size[0] // 2
        # Tile from top to bottom, slightly past image height to avoid edge artifacts
        y = -tile.size[1] // 2
        while y < h + tile.size[1]:
            overlay.paste(tile, (x, y), tile)
            y += row_step

    # Slight blur (radius = 0.5 × scale)
    blur_radius = BLUR_SCALE * scale
    if blur_radius >= 0.5:
        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # Composite
    out = Image.alpha_composite(img.convert("RGBA"), overlay)
    out.convert("RGB").save(dst_path, "JPEG", quality=92, optimize=True)
    print(f"✅ {dst_path} ({w}x{h}) scale={scale:.3f} blur={blur_radius:.2f}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: watermark_cover.py <src> <dst> [long_edge]")
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2]
    edge = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    apply_watermark(src, dst, edge)