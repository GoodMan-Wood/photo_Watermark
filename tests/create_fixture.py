from PIL import Image
import os

out_dir = os.path.join('tests', 'fixtures')
os.makedirs(out_dir, exist_ok=True)
path = os.path.join(out_dir, 'test.jpg')
img = Image.new('RGB', (800, 600), color=(73, 109, 137))
img.save(path, quality=95)
print('Created test image:', path)
