import argparse
import sys
from .watermark import process_path


def parse_args(argv=None):
    p = argparse.ArgumentParser(description='Photo Watermark - 使用图片 EXIF 时间作为水印')
    p.add_argument('path', help='图片文件或目录路径')
    p.add_argument('--fontsize', type=int, default=36, help='字体大小（像素），默认 36')
    p.add_argument('--color', type=str, default='#FFFFFF', help='字体颜色，支持 #RRGGBB 或颜色名，默认 #FFFFFF')
    p.add_argument('--position', type=str, default='bottom-right', help='位置（例如 bottom-right, center, top-left），默认 bottom-right')
    p.add_argument('--font', type=str, default=None, help='字体文件路径（ttf）')
    p.add_argument('--use-mtime-if-no-exif', action='store_true', default=True, help='若无 EXIF 则使用文件修改时间（默认开启）')
    p.add_argument('--skip-no-time', action='store_true', help='若无时间信息则跳过该文件')
    p.add_argument('--margin', type=int, default=10, help='边距像素，默认 10')
    p.add_argument('--quality', type=int, default=95, help='JPEG 输出质量（1-100），默认 95')
    p.add_argument('--opacity', type=int, default=255, help='水印不透明度 (0-255)，默认 255 (不透明)')
    p.add_argument('--recursive', action='store_true', help='递归遍历目录')
    p.add_argument('--dry-run', action='store_true', help='预览但不写入文件')
    p.add_argument('--verbose', action='store_true', help='输出详细日志')
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    options = {
        'fontsize': args.fontsize,
        'color': args.color,
        'position': args.position,
        'font': args.font,
        'opacity': args.opacity,
        'use_mtime': args.use_mtime_if_no_exif,
        'skip_no_time': args.skip_no_time,
        'margin': args.margin,
        'quality': args.quality,
        'dry_run': args.dry_run,
        'verbose': args.verbose,
    }

    try:
        process_path(args.path, recursive=args.recursive, options=options)
    except KeyboardInterrupt:
        print('\nCancelled', file=sys.stderr)
        sys.exit(2)
