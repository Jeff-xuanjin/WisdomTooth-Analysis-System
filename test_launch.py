#!/usr/bin/env python3
"""
牙齿分割系统测试启动
验证所有模块都能正常导入
"""

import sys
import os
import traceback

def test_imports():
    """测试所有必要的导入"""
    print("🔍 测试模块导入...")
    print("=" * 60)
    
    tests = [
        ("PyQt5", "GUI框架"),
        ("ultralytics", "YOLOv8模型"),
        ("cv2", "OpenCV图像处理"),
        ("numpy", "数值计算"),
        ("matplotlib", "可视化"),
        ("PIL", "Pillow图像库"),
    ]
    
    all_passed = True
    for module, description in tests:
        try:
            if module == "cv2":
                import cv2
                version = cv2.__version__
            elif module == "PIL":
                from PIL import Image
                version = Image.__version__
            else:
                mod = __import__(module)
                version = getattr(mod, '__version__', '未知')
            
            print(f"✅ {description} ({module}): {version}")
        except ImportError as e:
            print(f"❌ {description} ({module}): 导入失败 - {e}")
            all_passed = False
    
    return all_passed

def test_paths():
    """测试路径设置"""
    print("\n📁 测试路径设置...")
    
    # 添加src目录到Python路径
    src_dir = os.path.join(os.path.dirname(__file__), "src")
    if os.path.exists(src_dir):
        sys.path.insert(0, src_dir)
        print(f"✅ src目录添加到路径: {src_dir}")
    else:
        print(f"❌ src目录不存在: {src_dir}")
        return False
    
    return True

def test_core_modules():
    """测试核心模块导入"""
    print("\n🧠 测试核心模块导入...")
    
    modules_to_test = [
        ("src.core.teeth_segmentor", "牙齿分割器"),
        ("src.gui.simple_gui", "GUI界面"),
        ("src.visualization.plotter", "可视化器"),
    ]
    
    for module_path, description in modules_to_test:
        try:
            # 动态导入
            if module_path == "src.gui.simple_gui":
                from src.gui import simple_gui
                print(f"✅ {description}: 导入成功")
            elif module_path == "src.core.teeth_segmentor":
                from src.core import teeth_segmentor
                print(f"✅ {description}: 导入成功")
            elif module_path == "src.visualization.plotter":
                from src.visualization import plotter
                print(f"✅ {description}: 导入成功")
        except ImportError as e:
            print(f"❌ {description}: 导入失败 - {e}")
            traceback.print_exc()
            return False
    
    return True

def test_gui_import():
    """测试GUI模块的Qt导入"""
    print("\n🖥️  测试GUI模块的Qt导入...")
    
    try:
        # 测试Qt导入
        from PyQt5.QtCore import Qt
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QPixmap
        
        print(f"✅ Qt.AlignCenter = {Qt.AlignCenter}")
        print(f"✅ Qt.Horizontal = {Qt.Horizontal}")
        
        # 尝试创建虚拟应用
        app = QApplication.instance() or QApplication([])
        print("✅ QApplication创建成功")
        
        return True
    except Exception as e:
        print(f"❌ Qt导入测试失败: {e}")
        traceback.print_exc()
        return False

def test_model_file():
    """测试模型文件"""
    print("\n🤖 测试模型文件...")
    
    model_paths = [
        "./models/weights/best.pt",
        "./models/training/yolov8s-seg.pt",
        "yolov8s-seg.pt"
    ]
    
    found = False
    for path in model_paths:
        if os.path.exists(path):
            found = True
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"✅ 找到模型: {path} ({size_mb:.1f}MB)")
            break
    
    if not found:
        print("❌ 未找到模型文件！")
        print("请将模型文件放在以下位置之一:")
        for path in model_paths:
            print(f"  - {path}")
    
    return found

def main():
    """主测试函数"""
    print("=" * 60)
    print("🦷 牙齿分割系统启动测试")
    print("=" * 60)
    
    all_tests_passed = True
    
    # 运行所有测试
    if not test_imports():
        all_tests_passed = False
    
    if not test_paths():
        all_tests_passed = False
    
    if not test_core_modules():
        all_tests_passed = False
    
    if not test_gui_import():
        all_tests_passed = False
    
    if not test_model_file():
        all_tests_passed = False
    
    print("\n" + "=" * 60)
    
    if all_tests_passed:
        print("✅ 所有测试通过！")
        print("可以启动牙齿分割系统了")
        
        # 询问是否立即启动
        print("\n是否立即启动系统？(y/n)")
        choice = input().strip().lower()
        if choice == 'y':
            launch_system()
    else:
        print("❌ 部分测试失败，请检查上述错误")
        print("无法启动系统")

def launch_system():
    """启动系统"""
    print("\n🚀 启动牙齿分割系统...")
    print("=" * 60)
    
    try:
        # 导入并运行主程序
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from src.gui.simple_gui import main as gui_main
        
        print("✅ 导入GUI成功，正在启动...")
        gui_main()
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()