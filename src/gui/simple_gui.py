#!/usr/bin/env python3
"""
牙齿分割系统 - 完整极简GUI
包含真实的分割功能
"""

import sys
import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QTimer, QSize, QRect, QPoint, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QSplitter, QProgressBar, QDialog
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon, QColor, QPainter, QBrush, QPen, QPalette, QCursor, QTransform

class SimpleTeethGUI(QMainWindow):
    """完整的极简牙齿分割GUI"""
    
    def __init__(self):
        super().__init__()
        self.image_path = None
        self.model_path = None
        self.init_ui()
        self.find_model()
    
    def init_ui(self):
        """初始化界面"""
        # 窗口设置
        self.setWindowTitle("牙齿分割系统")
        self.setGeometry(100, 100, 1000, 600)
        
        # 中心部件
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # 标题
        title = QLabel("🦷 牙齿分割识别系统")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # 按钮区域
        self.create_buttons(layout)
        
        # 图片显示区域
        self.create_image_display(layout)
        
        # 状态栏
        self.status_label = QLabel("就绪 - 请选择牙片图片")
        self.status_label.setStyleSheet("padding: 5px; background-color: #f0f0f0;")
        layout.addWidget(self.status_label)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                font-size: 14px;
                padding: 8px 16px;
                border-radius: 4px;
                border: 1px solid #ccc;
            }
        """)
    
    def create_buttons(self, layout):
        """创建按钮区域"""
        btn_layout = QHBoxLayout()
        
        # 选择图片按钮
        self.select_btn = QPushButton("📁 选择牙片")
        self.select_btn.clicked.connect(self.select_image)
        self.select_btn.setToolTip("选择牙片图片文件")
        
        # 分割按钮
        self.segment_btn = QPushButton("🔍 分割识别")
        self.segment_btn.clicked.connect(self.segment_image)
        self.segment_btn.setEnabled(False)
        self.segment_btn.setToolTip("开始牙齿分割识别")
        
        # 保存按钮
        self.save_btn = QPushButton("💾 保存结果")
        self.save_btn.clicked.connect(self.save_result)
        self.save_btn.setEnabled(False)
        self.save_btn.setToolTip("保存分割结果图片")
        
        btn_layout.addWidget(self.select_btn)
        btn_layout.addWidget(self.segment_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
    
    def create_image_display(self, layout):
        """创建图片显示区域"""
        # 使用QSplitter实现可调整大小的分割窗口
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：原始图片
        self.original_label = QLabel("请选择牙片图片")
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setMinimumSize(400, 300)
        self.original_label.setStyleSheet("""
            QLabel {
                border: 2px solid #ccc;
                background-color: #f8f9fa;
                color: #666;
                padding: 20px;
                font-size: 14px;
            }
        """)
        
        # 右侧：结果图片
        self.result_label = QLabel("分割结果将显示在这里")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setMinimumSize(400, 300)
        self.result_label.setStyleSheet("""
            QLabel {
                border: 2px solid #ccc;
                background-color: #f8f9fa;
                color: #666;
                padding: 20px;
                font-size: 14px;
            }
        """)
        
        splitter.addWidget(self.original_label)
        splitter.addWidget(self.result_label)
        splitter.setSizes([500, 500])
        
        layout.addWidget(splitter, 1)  # 1表示可扩展
    
    def find_model(self):
        """查找模型文件"""
        model_paths = [
            "./models/weights/best.pt",
            "./models/training/yolov8s-seg.pt",
            "yolov8s-seg.pt"
        ]
        
        for path in model_paths:
            if os.path.exists(path):
                self.model_path = path
                print(f"✅ 找到模型: {path}")
                return
        
        print("⚠️ 未找到模型文件")
    
    def select_image(self):
        """选择牙片图片"""
        # 文件选择对话框
        path, _ = QFileDialog.getOpenFileName(
            self, "选择牙片图片", "", 
            "图片文件 (*.jpg *.jpeg *.png *.bmp);;所有文件 (*.*)"
        )
        
        if path and os.path.exists(path):
            self.image_path = path
            
            # 显示原始图片
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                # 调整大小以适应显示
                scaled = pixmap.scaled(
                    self.original_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.original_label.setPixmap(scaled)
                
                # 更新状态
                filename = os.path.basename(path)
                self.status_label.setText(f"已选择: {filename}")
                self.segment_btn.setEnabled(True)
                
                # 清空之前的結果
                self.result_label.clear()
                self.result_label.setText("分割结果将显示在这里")
                self.save_btn.setEnabled(False)
            else:
                QMessageBox.warning(self, "警告", "无法加载图片")
    
    def segment_image(self):
        """执行牙齿分割"""
        if not self.image_path:
            QMessageBox.warning(self, "警告", "请先选择图片")
            return
        
        if not self.model_path or not os.path.exists(self.model_path):
            QMessageBox.warning(self, "警告", "未找到模型文件")
            return
        
        # 显示处理状态
        self.status_label.setText("正在处理，请稍候...")
        QApplication.processEvents()  # 更新UI
        
        try:
            # 记录开始时间
            start_time = time.time()
            
            # 1. 导入必要的库
            from ultralytics import YOLO
            import cv2
            import numpy as np
            
            # 2. 加载模型
            model = YOLO(self.model_path)
            
            # 3. 进行预测（使用固定轻量配置）
            print("🔍 开始牙齿分割...")
            results = model.predict(
                source=self.image_path,
                imgsz=320,       # 固定低分辨率
                conf=0.2,        # 低置信度阈值
                device='cpu',    # 使用CPU
                verbose=False,   # 不显示详细输出
                max_det=20,      # 最大检测数量
                retina_masks=True,  # 高质量掩码
            )
            
            # 4. 处理结果
            if not results or len(results) == 0 or results[0].masks is None:
                self.status_label.setText("未检测到牙齿")
                QMessageBox.information(self, "结果", "未检测到牙齿")
                return
            
            result = results[0]
            masks = result.masks.data.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            
            num_teeth = len(masks)
            process_time = time.time() - start_time
            
            print(f"✅ 检测到 {num_teeth} 个牙齿，耗时: {process_time:.1f}秒")
            
            # 5. 生成结果图片
            result_image = self.create_result_image(result.orig_img, masks, class_ids)
            
            if result_image is not None:
                # 显示结果图片
                self.display_result_image(result_image)
                
                # 更新状态
                self.status_label.setText(f"✅ 完成！检测到 {num_teeth} 个牙齿 (耗时: {process_time:.1f}秒)")
                self.save_btn.setEnabled(True)
                self.result_image_data = result_image
            else:
                self.status_label.setText("生成结果图片失败")
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ 分割失败: {error_msg}")
            QMessageBox.critical(self, "错误", f"分割失败:\n{error_msg}")
            self.status_label.setText(f"错误: {error_msg[:50]}")
    
    def create_result_image(self, image, masks, class_ids):
        """创建结果可视化图片"""
        try:
            import cv2
            import numpy as np
            import matplotlib.pyplot as plt
            
            # 确保图片是RGB格式
            if len(image.shape) == 3 and image.shape[2] == 3:
                if image.dtype == np.uint8:
                    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    img_rgb = image
            else:
                img_rgb = image
            
            # 创建简单的结果图片
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
            
            # 左侧：原始图片
            ax1.imshow(img_rgb)
            ax1.set_title('原始牙片')
            ax1.axis('off')
            
            # 右侧：分割结果
            if len(masks) > 0:
                # 创建颜色叠加
                overlay = image.copy()
                colors = [(0, 255, 0), (255, 0, 0)]  # 绿色和红色
                
                for i, (mask, class_id) in enumerate(zip(masks, class_ids)):
                    color = colors[class_id] if class_id < len(colors) else (128, 128, 128)
                    mask_bool = mask > 0.5
                    overlay[mask_bool] = color
                
                result_img = cv2.addWeighted(image, 0.6, overlay, 0.4, 0)
                result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                
                # 添加检测数量文本
                second_molars = np.sum(class_ids == 0)
                third_molars = np.sum(class_ids == 1)
                title_text = f'分割结果\n总牙齿: {len(masks)}'
                if second_molars > 0:
                    title_text += f'\n第二磨牙: {second_molars}'
                if third_molars > 0:
                    title_text += f'\n第三磨牙: {third_molars}'
                
                ax2.set_title(title_text)
            else:
                result_img_rgb = img_rgb
                ax2.set_title('无检测结果')
            
            ax2.imshow(result_img_rgb)
            ax2.axis('off')
            
            plt.suptitle('牙齿分割分析结果', fontsize=12)
            plt.tight_layout()
            
            # 将matplotlib图形转换为numpy数组
            fig.canvas.draw()
            width, height = fig.canvas.get_width_height()
            image_array = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            image_array = image_array.reshape(height, width, 3)
            
            plt.close(fig)
            return image_array
            
        except Exception as e:
            print(f"❌ 创建结果图片失败: {e}")
            return None
    
    def display_result_image(self, image_array):
        """显示numpy数组格式的图片"""
        try:
            height, width, channel = image_array.shape
            bytes_per_line = 3 * width
            
            # 转换为QImage
            qimage = QImage(image_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # 转换为QPixmap
            pixmap = QPixmap.fromImage(qimage)
            
            # 缩放以适应标签
            scaled = pixmap.scaled(
                self.result_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            self.result_label.setPixmap(scaled)
            
        except Exception as e:
            print(f"❌ 显示结果图片失败: {e}")
    
    def save_result(self):
        """保存结果图片"""
        if not hasattr(self, 'result_image_data') or self.result_image_data is None:
            QMessageBox.warning(self, "警告", "没有可保存的结果")
            return
        
        # 生成默认文件名
        default_name = "牙齿分割结果"
        if self.image_path:
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]
            default_name = f"{base_name}_分割结果"
        
        # 文件保存对话框
        path, _ = QFileDialog.getSaveFileName(
            self, "保存结果", default_name,
            "PNG图片 (*.png);;JPEG图片 (*.jpg);;所有文件 (*.*)"
        )
        
        if path:
            try:
                import cv2
                
                # 保存图片
                result_image = self.result_image_data
                result_image_bgr = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(path, result_image_bgr)
                
                QMessageBox.information(self, "成功", f"结果已保存到:\n{path}")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败:\n{e}")
    
    def closeEvent(self, event):
        """关闭窗口事件"""
        reply = QMessageBox.question(
            self, '确认退出',
            '确定要退出牙齿分割系统吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    """启动应用程序"""
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle("Fusion")
    
    # 设置应用程序信息
    app.setApplicationName("牙齿分割识别系统")
    app.setOrganizationName("牙齿分割研究")
    
    # 创建并显示主窗口
    window = SimpleTeethGUI()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()