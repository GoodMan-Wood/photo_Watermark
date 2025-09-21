# Photo Watermark — 项目控制文档

概述

- 该命令行工具用于从图片 EXIF 的拍摄时间中提取年月日，并将其作为文本水印绘制到图片上，保存至原目录下名为 "<原目录>_watermark" 的子目录。

主要需求

1. 用户输入一个图片文件路径（支持单文件或目录）。
2. 对路径下的所有图片文件读取 EXIF 的拍摄时间信息，选取年月日作为水印文本。
3. 用户可设置字体大小、颜色以及文本在图片上的位置（例如：左上角、居中、右下角）。
4. 程序将文本水印绘制到图片上，并保存为新的图片文件，保存在原目录名_watermark 的新子目录内。

输入/输出

- 输入：
  - 必需：图片文件或目录路径（命令行位置参数）。
  - 可选：字体大小、颜色、位置、字体文件路径、是否递归、输出质量等。
- 输出：
  - 在原目录下创建子目录 `<原目录>_watermark`（若不存在），将处理后的图片保存至此目录。

技术选型

- 语言：Python 3.8+
- 库：
  - Pillow — 图像处理与文本绘制
  - piexif 或使用 Pillow 的 EXIF 支持 — 读取 EXIF
  - tqdm — 进度条（可选）
  - webcolors — 解析颜色名（可选）

行为细节与边界条件

- 支持格式：JPEG, JPG, PNG（PNG 往往无 EXIF）
- EXIF 时间优先：DateTimeOriginal -> DateTime；若无 EXIF，则默认使用文件修改时间（可通过参数改为跳过）。
- 时间格式：YYYY-MM-DD
- 字体：允许用户提供 TTF 字体路径，否则使用系统默认字体（如 Windows 的 Arial 或 Pillow 提供的默认字体）。
- 位置：支持预定义 9 个位置（top-left, top-center, top-right, center-left, center, center-right, bottom-left, bottom-center, bottom-right），并支持自定义坐标（x,y）。
- 输出文件命名：原文件名 + `_wm` 后缀，或保留原名（可通过参数配置）。

CLI 设计（示例）

用法：

```
python photo_watermark.py <path> [--fontsize SIZE] [--color COLOR] [--position POS] [--font FONT_PATH] [--use-mtime-if-no-exif] [--skip-no-time] [--margin PIXELS] [--quality INT] [--recursive] [--workers N] [--dry-run] [--verbose]
```

参数示例解释：
- `path`：图片文件或目录路径
- `--fontsize`：字体大小，默认 36
- `--color`：字体颜色，支持 `#RRGGBB` 或颜色名，默认 `#FFFFFF`
- `--position`：位置字符串，默认 `bottom-right`
- `--font`：字体文件路径（.ttf）
- `--use-mtime-if-no-exif`：若无 EXIF 则使用文件修改时间（默认开启）
- `--skip-no-time`：若无时间信息则跳过（若两者同时出现，`use-mtime` 优先）
- `--margin`：边距像素，默认 10
- `--quality`：JPEG 输出质量（1-100），默认 95
- `--recursive`：递归遍历目录
- `--workers`：并发线程数（可选）
- `--dry-run`：预览但不写入文件
- `--verbose`：输出详细日志

核心模块契约（简述）

- extract_date_from_image(path) -> Optional[date]
  - 从图片中提取 DateTimeOriginal 或 DateTime，返回 date 对象或 None。
- render_watermark(img: PIL.Image, text: str, font_path: Optional[str], size:int, color:str, position:str, margin:int, shadow:bool) -> PIL.Image
  - 在图像上绘制文本并返回新的图像对象。
- process_file(path, out_dir, options) -> Optional[path]
  - 完成文件处理（读取 EXIF、生成文本、绘制、保存），返回输出路径或 None。

测试计划

- 单元测试：
  - EXIF 解析函数测试（含 DateTimeOriginal、无 EXIF 情况）
  - 位置与坐标计算测试
  - process_file 的集成测试（在临时目录上验证输出）
- 集成测试：在一组示例图片上运行 CLI 并验证输出目录结构和文件数量

交付物

- `photo_watermark/` 源代码包（含 CLI、核心模块、工具函数）
- `requirements.txt`
- `PROJECT_CONTROL.md`（当前文档）
- `tests/` 测试用例

下一步与扩展建议

- 提供 `--watermark-template` 支持更复杂的水印（例如：拍摄地点 + 时间，或自定义文本）
- 支持图像批量并发加速
- 自动选择对比色（基于局部背景颜色）以保证可读性

---

*文件已创建为 `PROJECT_CONTROL.md`。*
