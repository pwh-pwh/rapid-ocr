#!/usr/bin/env python3
"""
RapidOCR 图片文字识别脚本 (优化版)
用法: cd /home/pwh/aiwork/paddleocrdm && uv run python scripts/ocr_rapid.py <image_path>
"""
import sys
import os
import json
import urllib.request
import subprocess
import time

os.chdir("/home/pwh/aiwork/paddleocrdm")

OCR_SERVER = "http://127.0.0.1:9898/ocr"


def is_server_running() -> bool:
    """检查服务是否运行"""
    try:
        data = json.dumps({"image_path": ""}).encode()
        req = urllib.request.Request(OCR_SERVER, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=2) as resp:
            return True
    except urllib.error.HTTPError:
        return True  # 服务在运行，只是参数错误
    except:
        return False


def start_server():
    """启动常驻服务"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(script_dir, "ocr_server.py")
    subprocess.Popen(
        ["uv", "run", "python", server_script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # 等待服务启动
    for _ in range(10):
        time.sleep(1)
        if is_server_running():
            return True
    return False


def recognize_via_server(image_path: str) -> list:
    """通过常驻服务识别"""
    try:
        data = json.dumps({"image_path": image_path}).encode()
        req = urllib.request.Request(OCR_SERVER, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result.get("texts", [])
    except:
        return None


def recognize_direct(image_path: str) -> list:
    """直接识别（备用）"""
    import logging
    os.environ["ORT_LOG_LEVEL"] = "3"
    logging.getLogger("OrtInferSession").setLevel(logging.ERROR)
    
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR(
        det_use_cuda=False,
        rec_use_cuda=False,
        cls_use_cuda=False,
        use_cls=False,
        max_side_len=640,
    )
    result, _ = ocr(image_path)
    if result is None:
        return []
    return [item[1] for item in result]


def main():
    if len(sys.argv) < 2:
        print("用法: uv run python scripts/ocr_rapid.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path) and not image_path.startswith(("http://", "https://")):
        print(f"错误: 图片不存在 - {image_path}")
        sys.exit(1)
    
    # 自动启动服务（如果未运行）
    if not is_server_running():
        start_server()
    
    # 优先使用常驻服务
    results = recognize_via_server(image_path)
    
    # 服务不可用时直接识别
    if results is None:
        results = recognize_direct(image_path)
    
    if results:
        print("\n".join(results))


if __name__ == "__main__":
    main()
