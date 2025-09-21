# Implementation Plan — Photo Watermark

目的

- 给出详细的实现计划，包含需要创建的源文件、依赖、CLI 细节、测试用例与快速开发步骤，便于下一步开始编码实现 MVP（最小可行产品）。

要创建的文件结构（建议）

```
photo_watermark/
  __init__.py
  __main__.py        # 入口，允许 python -m photo_watermark
  cli.py             # 命令行参数解析
  watermark.py       # 核心逻辑：读取 EXIF、生成水印文本、绘制并保存
  utils.py           # 颜色解析、位置计算、文件工具等
  resources/
    default_font.ttf # 可选：随包分发的默认字体（注意许可）
requirements.txt
PROJECT_CONTROL.md
ASSUMPTIONS.md
IMPLEMENTATION_PLAN.md
tests/
  test_extract_date.py
  test_render_watermark.py
  test_process_file.py
```

首个 MVP 功能（必须实现）

- 支持处理单个图片文件或一个目录（默认非递归）；支持 `--recursive`。
- 从 EXIF 中提取 `DateTimeOriginal` 或 `DateTime`，如果没有则根据 `--use-mtime-if-no-exif` 使用 mtime，否则跳过。
- 支持 `--fontsize`, `--color`, `--position`，默认值分别为 36, `#FFFFFF`, `bottom-right`。
- 将文本绘制到图片并保存至源目录的子目录 `<source>_watermark`，默认保存为原名 + `_wm`。
- 在 Windows PowerShell 上可直接运行（注意路径与引号）。

依赖（requirements.txt）

- Pillow>=9.0
- piexif>=1.1.3 （可选：若使用 piexif 以更可靠地读写 EXIF）
- tqdm>=4.0 （可选：进度条）
- webcolors>=1.1.1 （可选：解析颜色名）

示例 CLI（PowerShell 风格）

```powershell
# 单文件
python .\photo_watermark\__main__.py "C:\photos\IMG_0001.jpg" --fontsize 36 --color "#FFFFFF" --position bottom-right

# 目录（递归）
python .\photo_watermark\__main__.py "C:\photos" --recursive --fontsize 28 --color white --position top-left
```

核心函数契约（更具体）

- extract_date_from_image(path: str) -> Optional[datetime.date]
  - 输入：图片路径
  - 输出：date 对象或 None
  - 错误行为：捕获异常并记录日志，返回 None

- render_watermark(img: PIL.Image.Image, text: str, font_path: Optional[str], fontsize: int, color: Tuple[int,int,int], position: str, margin: int, shadow: bool=False) -> PIL.Image.Image
  - 在图像上绘制文本并返回新图像对象（不直接修改原对象，或明确在文档说明）

- process_file(path: str, out_dir: str, options: dict) -> Optional[str]
  - 读取、提取时间、绘制并保存；返回输出文件路径或 None（若跳过）

位置计算（实现提示）

- 先测量文本宽高（draw.textsize）并依据位置和 margin 计算 x,y：
  - bottom-right：x = width - text_w - margin, y = height - text_h - margin
  - center：x = (width - text_w)/2, y = (height - text_h)/2
  - 其余类似

颜色与透明度

- 支持 `#RRGGBB` 与常见颜色名。若需要 alpha（透明度），在函数中暴露 `opacity` 参数（0-255）。对 JPEG，opacity 将影响合成后的像素；对 PNG 可通过 RGBA 层叠实现半透明文本。

测试与质量门

- 单元测试：
  - 使用临时目录与示例图片测试 `extract_date_from_image`、`render_watermark`、`process_file`。
  - 覆盖正常路径与无 EXIF 场景。
- Lint：基础的 flake8 或 pylint（可选）
- Smoke test：在 Windows PowerShell 上运行一次对一个示例目录的处理，验证输出目录存在且包含预期数量的文件。

开发步骤（快速指南）

1. 初始化虚拟环境并安装依赖：

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. 实现 `extract_date_from_image` 并用 1-2 张测试图片验证
3. 实现 `render_watermark`（使用 Pillow 的 ImageDraw 与 ImageFont）并在多张图片上调试位置、颜色
4. 实现 `process_file`、CLI 并把文件保存到 `<src>_watermark`
5. 添加单元测试并运行 `pytest`（或前期使用简单脚本验证）

交付与后续

- 完成 MVP 后，提交代码并运行测试。随后可扩展：并发处理、自动对比色、更多格式支持、EXIF 写回。
