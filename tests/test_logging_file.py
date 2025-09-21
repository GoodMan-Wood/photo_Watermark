import os
import shutil
import tempfile
from PIL import Image


def test_cli_writes_logfile():
    tmp = tempfile.mkdtemp()
    try:
        src = os.path.join(tmp, 'src')
        os.makedirs(src, exist_ok=True)
        path = os.path.join(src, 'img.jpg')
        Image.new('RGB', (120, 80), color=(20, 30, 40)).save(path)
        logfile = os.path.join(tmp, 'process.log')

        # call CLI main programmatically
        from photo_watermark.cli import main
        # Use dry-run so it will not write images but still produce stats
        main([path, '--logfile', logfile, '--dry-run'])

        assert os.path.exists(logfile)
        content = open(logfile, 'r', encoding='utf-8').read()
        assert 'Processed:' in content or 'Processed' in content
    finally:
        shutil.rmtree(tmp)
