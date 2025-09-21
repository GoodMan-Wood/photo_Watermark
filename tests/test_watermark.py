import os
import shutil
import tempfile
from PIL import Image
from photo_watermark.watermark import extract_date_from_image, render_watermark, process_file


def test_extract_date_none_for_plain_jpg():
    tmp = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp, 'noexif.jpg')
        Image.new('RGB', (100, 100), color=(255, 0, 0)).save(path)
        assert extract_date_from_image(path) is None
    finally:
        shutil.rmtree(tmp)


def test_render_watermark_returns_image():
    img = Image.new('RGB', (200, 100), color=(10, 10, 10))
    out = render_watermark(img, '2025-09-21', None, 20, (255, 255, 255), 'center', 5, opacity=128)
    assert hasattr(out, 'size')
    assert out.size == img.size


def test_process_file_creates_output():
    tmp = tempfile.mkdtemp()
    try:
        src = os.path.join(tmp, 'src')
        os.makedirs(src, exist_ok=True)
        path = os.path.join(src, 'img.jpg')
        Image.new('RGB', (300, 200), color=(0, 128, 255)).save(path)
        options = {
            'fontsize': 16,
            'color': '#FFFFFF',
            'position': 'bottom-right',
            'font': None,
            'use_mtime': True,
            'skip_no_time': False,
            'margin': 5,
            'dry_run': False,
            'quality': 90,
            'verbose': False,
            'opacity': 200,
        }
        out_path = process_file(path, options)
        parent = os.path.dirname(os.path.abspath(src))
        dirname = os.path.basename(os.path.abspath(src))
        expected_dir = os.path.join(parent, f"{dirname}_watermark")
        assert os.path.isdir(expected_dir)
        files = os.listdir(expected_dir)
        assert any(f.endswith('_wm.jpg') for f in files)
    finally:
        shutil.rmtree(tmp)


def test_process_path_with_workers():
    tmp = tempfile.mkdtemp()
    try:
        src = os.path.join(tmp, 'srcdir')
        os.makedirs(src, exist_ok=True)
        # create multiple files
        for i in range(4):
            Image.new('RGB', (100 + i * 10, 100), color=(i * 20, 50, 100)).save(os.path.join(src, f'img{i}.jpg'))
        options = {'fontsize': 12, 'color': '#FFFFFF', 'position': 'bottom-right', 'font': None, 'use_mtime': True, 'skip_no_time': False, 'margin': 5, 'dry_run': False, 'quality': 80, 'verbose': False, 'opacity': 255}
        from photo_watermark.watermark import process_path
        process_path(src, recursive=False, options=options, workers=3)
        parent = os.path.dirname(os.path.abspath(src))
        dirname = os.path.basename(os.path.abspath(src))
        expected_dir = os.path.join(parent, f"{dirname}_watermark")
        assert os.path.isdir(expected_dir)
        files = os.listdir(expected_dir)
        assert len([f for f in files if f.endswith('_wm.jpg')]) == 4
    finally:
        shutil.rmtree(tmp)


def test_process_path_returns_stats():
    tmp = tempfile.mkdtemp()
    try:
        src = os.path.join(tmp, 'one')
        os.makedirs(src, exist_ok=True)
        path = os.path.join(src, 'a.jpg')
        Image.new('RGB', (50, 50), color=(10, 10, 10)).save(path)
        options = {'fontsize': 12, 'color': '#FFF', 'position': 'center', 'font': None, 'use_mtime': True, 'skip_no_time': False, 'margin': 2, 'dry_run': True, 'quality': 80, 'verbose': False, 'opacity': 255}
        from photo_watermark.watermark import process_path
        stats = process_path(src, recursive=False, options=options, workers=1)
        assert isinstance(stats, dict)
        assert set(stats.keys()) == {'success', 'failed', 'skipped'}
    finally:
        shutil.rmtree(tmp)
