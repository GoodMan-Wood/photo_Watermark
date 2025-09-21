
# Photo Watermark

一个用于把图片 EXIF 拍摄时间（年月日）作为文本水印绘制到图片上的命令行工具。该工具使用 Python 和 Pillow 实现，支持从 EXIF 提取时间或使用文件修改时间作为备选，并将带水印的图片保存到源目录的同级目录（`<dirname>_watermark`）。

## 功能

- 从图片 EXIF 中提取 `DateTimeOriginal`（或 `DateTime`）并格式化为 `YYYY-MM-DD` 作为水印文本。
- 支持字体大小、颜色、位置、边距、JPEG 输出质量等参数。
- 支持处理单个文件或目录（可递归）。
- 保持原图不覆盖，输出为 `<原名>_wm.<ext>`，保存在与原目录并列的 `<dirname>_watermark` 目录中。

## 依赖

- Python 3.8+
- Pillow>=9.0

可选依赖：`piexif`, `tqdm`, `webcolors`（用于扩展功能）

安装依赖：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 快速开始

生成并处理一张测试图片（示例）：

```powershell
python .\tests\create_fixture.py
python -m photo_watermark .\tests\fixtures\test.jpg --verbose
```

处理目录示例：

```powershell
python -m photo_watermark "C:\path\to\photos" --recursive --fontsize 28 --color "#FFFF00" --position top-left
```

## CLI 参数

```
usage: __main__.py [-h] [--fontsize FONTSIZE] [--color COLOR]
									 [--position POSITION] [--font FONT]
									 [--use-mtime-if-no-exif] [--skip-no-time]
									 [--margin MARGIN] [--quality QUALITY] [--recursive]
									 [--dry-run] [--verbose]
									 path
```

常用参数：
- `path`：要处理的图片文件或目录路径
- `--fontsize`：字体大小（像素），默认 36
- `--color`：字体颜色，支持 `#RRGGBB` 或常见颜色名，默认 `#FFFFFF`
- `--position`：位置（例如 `bottom-right`, `center`, `top-left`），默认 `bottom-right`
- `--font`：字体文件路径（TTF），若未提供使用系统字体或 Pillow 默认字体
- `--use-mtime-if-no-exif`：无 EXIF 时使用文件修改时间（默认开启）
- `--skip-no-time`：无时间信息时跳过该文件
- `--margin`：边距（像素），默认 10
- `--quality`：JPEG 输出质量（1-100），默认 95
- `--recursive`：递归处理目录
- `--dry-run`：仅预览不写入
- `--verbose`：显示详细日志
- `--logfile`：将日志写入到指定文件（追加模式），例如 `--logfile C:\logs\process.log`

## 运行测试

运行 pytest（在项目根目录）：

```powershell
$env:PYTHONPATH = '.'; pytest -q
```

## 项目结构

```
photo_watermark/
	__init__.py
	__main__.py
	cli.py
	watermark.py
	utils.py
requirements.txt
tests/
	create_fixture.py
	fixtures/
	fixtures_watermark/
	test_watermark.py
PROJECT_CONTROL.md
ASSUMPTIONS.md
IMPLEMENTATION_PLAN.md
README.md
```

## 后续改进

- 更健壮的字体加载与内置字体分发
- 支持文字透明度（opacity）、自动对比色
- 并发批量处理（--workers）
- 保留或回写 EXIF（使用 piexif）

---

### 日志到文件示例

在 Windows PowerShell 中将日志写入文件并显示控制台输出的示例：

```powershell
# 指定 logfile，同时显示控制台输出
python -m photo_watermark "C:\path\to\photos" --recursive --log INFO --logfile "C:\temp\photo_process.log"
```

日志文件采用追加模式（append），编码为 UTF-8。若需要日志轮替或按大小分割，请告诉我，我可以添加 `RotatingFileHandler` 支持。
