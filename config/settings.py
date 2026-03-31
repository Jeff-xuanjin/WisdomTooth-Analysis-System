#!/usr/bin/env python3
"""
牙齿分割系统 - 配置文件
集中管理所有参数和设置
"""

import os
from pathlib import Path

# ========== 项目基本信息 ==========
PROJECT_NAME = "牙齿分割识别系统"
VERSION = "1.0.0"
AUTHOR = "牙齿分割开发团队"
DESCRIPTION = "基于YOLOv8的牙齿分割识别系统"

# ========== 路径配置 ==========
# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 数据路径
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ANNOTATIONS_DIR = DATA_DIR / "annotations"

# 模型路径
MODELS_DIR = BASE_DIR / "models"
WEIGHTS_DIR = MODELS_DIR / "weights"
TRAINING_DIR = MODELS_DIR / "training"

# 结果路径
RESULTS_DIR = BASE_DIR / "results"
LOGS_DIR = BASE_DIR / "logs"

# 资源路径
RESOURCES_DIR = BASE_DIR / "resources"

# ========== 模型配置 ==========
MODEL_CONFIG = {
    # 模型路径（按优先级查找）
    "model_paths": [
        str(WEIGHTS_DIR / "best.pt"),        # 第一优先级
        str(TRAINING_DIR / "yolov8s-seg.pt"),  # 第二优先级
        "yolov8s-seg.pt",                    # 第三优先级
    ],
    
    # 推理参数
    "imgsz": 320,           # 输入图像尺寸
    "conf": 0.2,           # 置信度阈值
    "iou": 0.45,           # IoU阈值
    "max_det": 20,         # 最大检测数量
    
    # 性能优化
    "device": "cpu",       # 使用CPU
    "half": True,         # 使用半精度
    "verbose": False,     # 静默模式
    "retina_masks": True, # 使用高质量掩码
    "agnostic_nms": True, # 类别无关NMS
}

# ========== 可视化配置 ==========
VISUALIZATION_CONFIG = {
    # 颜色配置
    "colors": {
        0: (0, 255, 0),    # 第二磨牙 - 绿色
        1: (255, 0, 0),    # 第三磨牙 - 红色
    },
    
    # 文本配置
    "font_scale": 0.8,     # 字体大小
    "thickness": 2,        # 线宽
    
    # 图片质量
    "jpeg_quality": 85,    # JPEG保存质量
    "png_compression": 3,  # PNG压缩级别
    
    # 图形配置
    "figsize": (12, 6),    # 图形大小
    "dpi": 100,            # 分辨率
}

# ========== GUI配置 ==========
GUI_CONFIG = {
    # 窗口配置
    "window_size": (1200, 700),  # 窗口大小
    "window_title": "牙齿分割识别系统",
    
    # 图片显示
    "max_preview_size": (600, 400),  # 最大预览尺寸
    "default_preview_text": "请选择牙片图像",  # 默认文本
    
    # 按钮样式
    "button_style": {
        "normal": """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """,
        "danger": """
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """,
    },
    
    # 标签样式
    "label_style": """
        QLabel {
            border: 2px solid #ccc;
            background-color: #f8f9fa;
            font-size: 14px;
            color: #666;
            padding: 20px;
        }
    """,
}

# ========== 系统配置 ==========
SYSTEM_CONFIG = {
    # 日志配置
    "log_level": "INFO",  # 日志级别
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": str(LOGS_DIR / "teeth_segmentation.log"),
    
    # 性能配置
    "max_workers": 1,      # 最大工作线程
    "timeout": 30,         # 超时时间（秒）
    "memory_limit_mb": 512,  # 内存限制
    
    # 文件处理
    "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".tiff"],
    "max_file_size_mb": 10,  # 最大文件大小
}

# ========== 应用配置 ==========
APP_CONFIG = {
    "name": PROJECT_NAME,
    "version": VERSION,
    "author": AUTHOR,
    "description": DESCRIPTION,
    
    # 功能开关
    "enable_save": True,        # 是否启用保存功能
    "enable_batch": False,      # 是否启用批量处理
    "enable_stats": True,       # 是否启用统计
    "enable_export": True,      # 是否启用导出
}

# ========== 实用函数 ==========
def get_model_path():
    """获取模型路径（自动查找）"""
    for path in MODEL_CONFIG["model_paths"]:
        if os.path.exists(path):
            return path
    return None

def get_config_summary():
    """获取配置摘要"""
    summary = {
        "project": f"{PROJECT_NAME} v{VERSION}",
        "model": {
            "imgsz": MODEL_CONFIG["imgsz"],
            "conf": MODEL_CONFIG["conf"],
            "device": MODEL_CONFIG["device"],
        },
        "paths": {
            "model": get_model_path(),
            "results": str(RESULTS_DIR),
            "logs": str(LOGS_DIR),
        }
    }
    return summary

def create_directories():
    """创建必要的目录"""
    directories = [
        DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, ANNOTATIONS_DIR,
        MODELS_DIR, WEIGHTS_DIR, TRAINING_DIR,
        RESULTS_DIR, LOGS_DIR, RESOURCES_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    print("✅ 目录结构已创建")

# ========== 环境特定配置 ==========
# 可以根据环境变量加载不同配置
ENV = os.getenv("TEETH_ENV", "development")

if ENV == "production":
    # 生产环境配置
    MODEL_CONFIG["verbose"] = False
    SYSTEM_CONFIG["log_level"] = "WARNING"
elif ENV == "development":
    # 开发环境配置
    MODEL_CONFIG["verbose"] = True
    SYSTEM_CONFIG["log_level"] = "DEBUG"
elif ENV == "testing":
    # 测试环境配置
    MODEL_CONFIG["conf"] = 0.1  # 更低置信度以便测试
    MODEL_CONFIG["imgsz"] = 256  # 更小尺寸以便快速测试

# 自动创建目录
try:
    create_directories()
except Exception as e:
    print(f"⚠️  创建目录失败: {e}")

# 配置验证
if __name__ == "__main__":
    print("=" * 50)
    print(f"{PROJECT_NAME} 配置检查")
    print("=" * 50)
    
    # 打印配置摘要
    summary = get_config_summary()
    for key, value in summary.items():
        print(f"\n📁 {key.upper()}:")
        if isinstance(value, dict):
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {value}")
    
    # 检查模型文件
    model_path = get_model_path()
    if model_path:
        print(f"\n✅ 找到模型: {model_path}")
    else:
        print(f"\n❌ 未找到模型文件")
        print("请将模型放在以下位置之一:")
        for path in MODEL_CONFIG["model_paths"]:
            print(f"  - {path}")
    
    print("\n" + "=" * 50)