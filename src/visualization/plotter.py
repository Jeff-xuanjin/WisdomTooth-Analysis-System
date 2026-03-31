#!/usr/bin/env python3
"""
轻量可视化器
固定配置，无需检测
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Optional

class LightPlotter:
    """轻量可视化器 - 固定配置"""
    
    def __init__(self):
        # 固定配置
        self.CONFIG = {
            "figsize": (10, 5),     # 小尺寸图像
            "dpi": 100,             # 低DPI
            "fontsize": 10,         # 小字体
            "quality": 0.7,         # 中等质量
        }
        
        # 简单字体配置
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 颜色定义
        self.colors = {
            0: (0, 200, 0),    # 浅绿色
            1: (200, 0, 0),    # 浅红色
        }
    
    def create_simple_result(self, results: Dict) -> Optional[np.ndarray]:
        """
        创建简单结果图 - 固定配置
        """
        if not results or 'image' not in results:
            return None
        
        try:
            image = results['image']
            masks = results.get('masks', [])
            class_ids = results.get('class_ids', [])
            
            # 创建简单子图
            fig, axes = plt.subplots(1, 2, figsize=self.CONFIG["figsize"], dpi=self.CONFIG["dpi"])
            
            # 1. 原始图像
            if len(image.shape) == 3:
                axes[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                axes[0].imshow(image, cmap='gray')
            axes[0].set_title('原始图像', fontsize=self.CONFIG["fontsize"])
            axes[0].axis('off')
            
            # 2. 分割结果
            overlay = self._create_simple_overlay(image, masks, class_ids)
            axes[1].imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
            
            num_teeth = len(masks) if masks is not None else 0
            axes[1].set_title(f'检测到 {num_teeth} 个牙齿', fontsize=self.CONFIG["fontsize"])
            axes[1].axis('off')
            
            plt.suptitle('牙齿分割结果', fontsize=self.CONFIG["fontsize"] + 2)
            plt.tight_layout()
            
            # 转换为numpy数组
            fig.canvas.draw()
            width, height = fig.canvas.get_width_height()
            image_array = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            image_array = image_array.reshape(height, width, 3)
            
            plt.close(fig)
            return image_array
            
        except Exception as e:
            print(f"❌ 可视化失败: {e}")
            return None
    
    def _create_simple_overlay(self, image, masks, class_ids):
        """创建简单颜色叠加"""
        if not masks or len(masks) == 0:
            return image
        
        overlay = image.copy()
        
        for mask, class_id in zip(masks, class_ids):
            color = self.colors.get(class_id, (128, 128, 128))
            mask_bool = mask > 0
            overlay[mask_bool] = color
        
        return cv2.addWeighted(image, 0.7, overlay, 0.3, 0)
    
    def create_quick_preview(self, results: Dict) -> Optional[np.ndarray]:
        """
        快速预览 - 最简化
        """
        if not results or 'image' not in results:
            return None
        
        image = results['image']
        masks = results.get('masks', [])
        
        # 直接在原图上绘制轮廓
        preview = image.copy()
        
        if masks and len(masks) > 0:
            for mask in masks:
                if mask is not None:
                    # 查找轮廓
                    mask_uint8 = (mask * 255).astype(np.uint8)
                    contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    if contours:
                        cv2.drawContours(preview, contours, -1, (0, 255, 0), 1)
        
        # 添加简单文字
        num_teeth = len(masks) if masks is not None else 0
        cv2.putText(preview, f"Teeth: {num_teeth}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return preview