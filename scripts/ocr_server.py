#!/usr/bin/env python3
"""
RapidOCR 常驻服务
用法: cd ~/.hermes/skills/rapidocr && uv run python scripts/ocr_server.py
端口: 9898
"""
import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(SKILL_DIR)

print("正在加载 OCR 模型...")
from rapidocr_onnxruntime import RapidOCR

ocr = RapidOCR(
    det_use_cuda=False,
    rec_use_cuda=False,
    cls_use_cuda=False,
    use_cls=False,
    max_side_len=640,
)
print("OCR 模型加载完成")


class OCRHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/ocr':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            image_path = data.get('image_path', '')
            if not os.path.exists(image_path):
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "图片不存在"}).encode())
                return
            
            result, _ = ocr(image_path)
            texts = [item[1] for item in result] if result else []
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"texts": texts}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # 禁用日志


def main():
    server = HTTPServer(('127.0.0.1', 9898), OCRHandler)
    print("OCR 服务已启动，监听端口 9898")
    server.serve_forever()


if __name__ == "__main__":
    main()
