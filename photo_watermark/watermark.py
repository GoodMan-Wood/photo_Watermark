import os
from datetime import datetime
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ExifTags
from .utils import parse_hex_color


def extract_date_from_image(path: str) -> Optional[datetime.date]:
    try:
        with Image.open(path) as img:
            exif = img.getexif()
            if exif:
                # Try DateTimeOriginal (36867) then DateTime (306)
                date_str = None
                if 36867 in exif:
                    date_str = exif.get(36867)
                elif 306 in exif:
                    date_str = exif.get(306)
                if date_str:
                    # EXIF date format: YYYY:MM:DD HH:MM:SS
                    try:
                        dt = datetime.strptime(str(date_str), '%Y:%m:%d %H:%M:%S')
                        return dt.date()
                    except Exception:
                        pass
            return None
    except Exception:
        return None


def _get_font(font_path: Optional[str], fontsize: int) -> ImageFont.FreeTypeFont:
    # Priority: user-provided font -> common system fonts -> Pillow default
    if font_path and os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, fontsize)
        except Exception:
            pass
    # Try several common fonts (Windows/DejaVu)
    for fname in ('arial.ttf', 'DejaVuSans.ttf', 'LiberationSans-Regular.ttf'):
        try:
            return ImageFont.truetype(fname, fontsize)
        except Exception:
            continue
    return ImageFont.load_default()


def render_watermark(img: Image.Image, text: str, font_path: Optional[str], fontsize: int, color: Tuple[int,int,int], position: str, margin: int, opacity: int = 255) -> Image.Image:
    # Ensure RGBA for compositing
    if img.mode != 'RGBA':
        base = img.convert('RGBA')
    else:
        base = img.copy()

    overlay = Image.new('RGBA', base.size, (255,255,255,0))
    draw = ImageDraw.Draw(overlay)
    font = _get_font(font_path, fontsize)

    text_w, text_h = draw.textsize(text, font=font)
    w, h = base.size

    pos = position.lower()
    if pos == 'bottom-right':
        x = w - text_w - margin
        y = h - text_h - margin
    elif pos == 'bottom-center' or pos == 'center-bottom':
        x = (w - text_w) // 2
        y = h - text_h - margin
    elif pos == 'bottom-left':
        x = margin
        y = h - text_h - margin
    elif pos == 'top-left':
        x = margin
        y = margin
    elif pos == 'top-center' or pos == 'center-top':
        x = (w - text_w) // 2
        y = margin
    elif pos == 'top-right':
        x = w - text_w - margin
        y = margin
    elif pos == 'center-left':
        x = margin
        y = (h - text_h) // 2
    elif pos == 'center-right':
        x = w - text_w - margin
        y = (h - text_h) // 2
    else:  # center
        x = (w - text_w) // 2
        y = (h - text_h) // 2

    r,g,b = color
    # draw with alpha
    draw.text((x, y), text, font=font, fill=(r, g, b, int(opacity)))

    out = Image.alpha_composite(base, overlay)
    # If original image had no alpha, convert back to RGB
    if img.mode != 'RGBA':
        out = out.convert(img.mode)
    return out


def process_file(path: str, options: dict) -> Optional[str]:
    # Determine date
    date = extract_date_from_image(path)
    if date is None and options.get('use_mtime', True):
        try:
            mtime = os.path.getmtime(path)
            date = datetime.fromtimestamp(mtime).date()
        except Exception:
            date = None
    if date is None:
        if options.get('skip_no_time'):
            if options.get('verbose'):
                print(f"Skipping {path}: no date available")
            return None
        else:
            if options.get('verbose'):
                print(f"No date for {path}, using 'unknown' text")
            text = 'unknown'
    else:
        text = date.strftime('%Y-%m-%d')

    try:
        with Image.open(path) as img:
            color = (255,255,255)
            try:
                color = parse_hex_color(options.get('color', '#FFFFFF'))
            except Exception:
                pass
            out_img = render_watermark(img, text, options.get('font'), options.get('fontsize',36), color, options.get('position','bottom-right'), options.get('margin',10), opacity=options.get('opacity',255))

            # Build output path: create sibling directory named <dirname>_watermark
            src_dir = os.path.dirname(path) or '.'
            abs_src = os.path.abspath(src_dir)
            parent_dir = os.path.dirname(abs_src)
            dirname = os.path.basename(abs_src)
            out_dir = os.path.join(parent_dir, f"{dirname}_watermark")
            os.makedirs(out_dir, exist_ok=True)

            base, ext = os.path.splitext(os.path.basename(path))
            out_name = f"{base}_wm{ext}"
            out_path = os.path.join(out_dir, out_name)

            if options.get('dry_run'):
                print(f"[dry-run] would write: {out_path}")
                return out_path

            save_kwargs = {}
            if ext.lower() in ['.jpg', '.jpeg']:
                save_kwargs['quality'] = options.get('quality', 95)
                out_img = out_img.convert('RGB')
            out_img.save(out_path, **save_kwargs)
            if options.get('verbose'):
                print(f"Saved watermarked image to: {out_path}")
            return out_path
    except Exception as e:
        if options.get('verbose'):
            print(f"Error processing {path}: {e}")
        return None


def process_path(path: str, recursive: bool=False, options: dict=None):
    if options is None:
        options = {}
    if os.path.isfile(path):
        process_file(path, options)
        return
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    full = os.path.join(root, f)
                    process_file(full, options)
            if not recursive:
                break
        return
    raise FileNotFoundError(path)
