# RapidOCR API 参考

## 基本用法

```python
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()
result, _ = engine("image.jpg")
```

## 返回格式

`result` 是一个列表，每项包含：
- `result[0]` - bbox: 文字区域坐标 `[[x1,y1], [x2,y2], [x3,y3], [x4,y4]]`
- `result[1]` - text: 识别到的文字
- `result[2]` - score: 置信度 (0-1)

示例：
```python
[
  [[[1275.0, 23.0], [1387.0, 23.0], [1387.0, 50.0], [1275.0, 50.0]], 'NO.30431', 0.9998],
  [[[149.0, 49.0], [384.0, 49.0], [384.0, 78.0], [149.0, 78.0]], '中国建设银行', 0.9994],
]
```

## 构造参数

```python
RapidOCR(
    config_path=None,      # 自定义配置文件路径
    det_use_cuda=False,    # 文字检测是否用GPU
    rec_use_cuda=False,    # 文字识别是否用GPU
    cls_use_cuda=False,    # 方向分类是否用GPU
    use_cls=False,         # 是否启用方向分类（禁用可加速）
    max_side_len=2000,     # 图片最大边长（越小越快，精度略降）
)
```

### 速度优化参数
| 参数 | 默认值 | 推荐值 | 效果 |
|------|--------|--------|------|
| `use_cls` | True | False | 禁用方向分类，减少模型加载 |
| `max_side_len` | 2000 | 640 | 缩小图片，~40%提速 |

实测数据（test.jpg，1400x700图片）：
- 默认配置: ~6s
- `use_cls=False, max_side_len=640`: ~3.6s

## 配置文件

默认配置路径: `.venv/lib/python3.13/site-packages/rapidocr_onnxruntime/config.yaml`

关键配置项：
```yaml
Global:
    text_score: 0.5        # 文字置信度阈值
    use_det: true          # 启用文字检测
    use_cls: true          # 启用方向分类
    use_rec: true          # 启用文字识别
    max_side_len: 2000     # 图片最大边长
    intra_op_num_threads: -1  # 线程数（-1=自动）
```

## 项目依赖

- `rapidocr_onnxruntime` - ONNX Runtime 后端
- `onnxruntime` - CPU版（默认安装）
- Python 3.13+
