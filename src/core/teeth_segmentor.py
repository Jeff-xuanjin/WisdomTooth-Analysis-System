#!/usr/bin/env python3
"""
牙齿分割器 - 固定轻量配置
专为轻薄笔记本优化，无性能检测
"""

import cv2
import numpy as np
from ultralytics import YOLO
import os
import time
from typing import Dict, Optional

class LightTeethSegmentor:
    """轻量牙齿分割器 - 固定配置"""
    
    def __init__(self, model_path: str = None):
        """
        初始化分割器 - 固定轻量配置
        配置: 320px分辨率, CPU, 半精度, 低置信度
        """
        # 固定轻量配置
        self.CONFIG = {
            "imgsz": 320,        # 低分辨率
            "conf": 0.2,         # 低置信度
            "half": True,        # 半精度
            "device": "cpu",     # 强制CPU
            "max_det": 20,       # 最大检测数
            "verbose": False,    # 静默模式
            "retina_masks": True,
            "agnostic_nms": True,  # 类别无关NMS
        }
        
        self.class_names = {0: '第二磨牙', 1: '第三磨牙'}
        
        print("🔧 初始化轻量分割器")
        print("📊 固定配置:")
        for key, value in self.CONFIG.items():
            print(f"   {key}: {value}")
        
        # 加载模型
        self.model = self._load_model(model_path)
        
        # 预热模型（CPU第一次推理较慢）
        self._warm_up()
    
    def _load_model(self, model_path: str) -> YOLO:
        """加载模型"""
        if model_path and os.path.exists(model_path):
            return YOLO(model_path)
        
        # 尝试查找模型
        for path in ["./models/weights/best.pt", "./models/training/yolov8s-seg.pt"]:
            if os.path.exists(path):
                print(f"✅ 加载模型: {path}")
                return YOLO(path)
        
        raise FileNotFoundError("❌ 未找到模型文件")
    
    def _warm_up(self):
        """预热模型"""
        print("🔥 预热模型...")
        try:
            # 创建一个小测试图像
            test_img = np.zeros((100, 100, 3), dtype=np.uint8)
            
            # 快速推理一次
            _ = self.model.predict(
                source=test_img,
                imgsz=160,
                conf=0.1,
                device='cpu',
                verbose=False,
                max_det=1
            )
            print("✅ 模型预热完成")
        except:
            print("⚠️  模型预热跳过")
    
    def segment(self, image_path: str) -> Optional[Dict]:
        """分割牙齿 - 使用固定轻量配置"""
        try:
            if not os.path.exists(image_path):
                print(f"❌ 文件不存在: {image_path}")
                return None
            
            filename = os.path.basename(image_path)
            print(f"🔍 处理: {filename}")
            
            # 记录开始时间
            start_time = time.time()
            
            # 使用固定配置进行推理
            results = self.model.predict(
                source=image_path,
                conf=self.CONFIG["conf"],
                imgsz=self.CONFIG["imgsz"],
                device=self.CONFIG["device"],
                half=self.CONFIG["half"],
                verbose=self.CONFIG["verbose"],
                max_det=self.CONFIG["max_det"],
                retina_masks=self.CONFIG["retina_masks"],
                agnostic_nms=self.CONFIG["agnostic_nms"],
            )
            
            # 计算处理时间
            process_time = time.time() - start_time
            
            if not results or not results[0].masks:
                print(f"⚠️  未检测到牙齿 (耗时: {process_time:.1f}s)")
                return None
            
            result = results[0]
            
            # 使用uint8减少内存
            masks = result.masks.data.cpu().numpy().astype(np.uint8)
            class_ids = result.boxes.cls.cpu().numpy().astype(np.uint8)
            
            num_teeth = len(masks)
            print(f"✅ 检测到 {num_teeth} 个牙齿 (耗时: {process_time:.1f}s)")
            
            # 统计各类数量
            for class_id, class_name in self.class_names.items():
                count = np.sum(class_ids == class_id)
                if count > 0:
                    print(f"   {class_name}: {count}个")
            
            return {
                'image': result.orig_img,
                'masks': masks,
                'class_ids': class_ids,
                'num_teeth': num_teeth,
                'process_time': process_time
            }
            
        except Exception as e:
            print(f"❌ 分割失败: {str(e)[:50]}")
            return None
    
    def get_config(self):
        """获取当前配置"""
        return self.CONFIG.copy()