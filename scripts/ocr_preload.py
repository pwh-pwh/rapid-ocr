#!/usr/bin/env python3
"""
RapidOCR 模型预加载脚本
用法: cd ~/.hermes/skills/paddleocr && uv run python scripts/ocr_preload.py
"""
import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(SKILL_DIR)

print("正在预加载 OCR 模型...")
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR(
    det_use_cuda=False,
    rec_use_cuda=False,
    cls_use_cuda=False,
    use_cls=False,
    max_side_len=640,
)
print("OCR 模型预加载完成")
