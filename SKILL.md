---
name: paddleocr
description: 使用RapidOCR识别图片中的文字，支持中英文识别。当用户在飞书发送图片并提到"识别图片"、"ocr"、"提取文字"等关键词时使用。
version: 2.3.0
---

# RapidOCR 图片文字识别

## 功能描述
使用RapidOCR识别图片中的文字，只返回识别到的文字内容，每行一条。

## 使用场景
当用户在飞书发送图片并提到以下关键词时触发：
- 识别图片
- OCR
- 提取文字
- 识别文字

## 执行步骤

### 1. 启动常驻服务（首次使用）
```bash
cd /home/pwh/aiwork/paddleocrdm && uv run python /home/pwh/.hermes/skills/paddleocr/scripts/ocr_server.py &
```

### 2. 执行OCR识别
```bash
cd /home/pwh/aiwork/paddleocrdm && uv run python /home/pwh/.hermes/skills/paddleocr/scripts/ocr_rapid.py <image_path>
```

### 3. 返回结果
直接返回识别到的文字，每行一条，不添加任何额外说明。

## 优化配置
- 常驻服务模式：模型只加载一次，后续识别约3秒
- 禁用方向分类 (`use_cls=False`)
- 减小最大边长 (`max_side_len=640`)

## 注意事项
1. 使用uv环境运行
2. 支持中英文混合识别
3. 图片路径可以是本地路径或URL
