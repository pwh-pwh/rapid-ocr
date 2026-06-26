#!/usr/bin/env python3
"""
RapidOCR 模型预加载脚本
用法: cd /home/pwh/aiwork/paddleocrdm && uv run python scripts/ocr_preload.py
"""
import os
import sys

os.chdir("/home/pwh/aiwork/paddleocrdm")

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
