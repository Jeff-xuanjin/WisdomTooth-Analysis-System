#!/usr/bin/env python3
"""
牙齿分割系统 - 轻量主程序
固定配置，无性能检测
"""

import sys
import os

def main():
    """主函数"""
    print("=" * 50)
    print("🦷 牙齿分割识别系统 (轻量固定配置)")
    print("=" * 50)
    
    print("\n📊 固定配置:")
    print("   分辨率: 320px")
    print("   置信度: 0.2")
    print("   设备: CPU")
    print("   半精度: 开启")
    print("   内存优化: 开启")
    print("=" * 50)
    
    # 快速检查
    print("\n🔍 检查文件...")
    
    # 检查关键文件
    required = [
        ("src/gui/simple_gui.py", "GUI界面"),
        ("src/core/teeth_segmentor.py", "分割器"),
        ("src/visualization/plotter.py", "可视化器"),
    ]
    
    all_ok = True
    for path, desc in required:
        if os.path.exists(path):
            print(f"✅ {desc}")
        else:
            print(f"❌ {desc}")
            all_ok = False
    
    # 检查模型
    model_found = False
    for path in ["./models/weights/best.pt", "./models/training/yolov8s-seg.pt"]:
        if os.path.exists(path):
            model_found = True
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"✅ 模型文件: {path} ({size_mb:.1f}MB)")
            break
    
    if not model_found:
        print("❌ 未找到模型文件")
        all_ok = False
    
    if not all_ok:
        print("\n⚠️  缺少必要文件，请检查!")
        input("按Enter键退出...")
        return
    
    # 检查依赖
    print("\n🔍 检查依赖...")
    
    deps = [
        ("PyQt5", "GUI界面"),
        ("ultralytics", "YOLO模型"),
        ("cv2", "OpenCV"),
        ("matplotlib", "可视化"),
    ]
    
    missing_deps = []
    for module, desc in deps:
        try:
            __import__(module)
            print(f"✅ {desc}")
        except ImportError:
            print(f"❌ {desc}")
            missing_deps.append(module)
    
    if missing_deps:
        print(f"\n⚠️  缺少依赖: {', '.join(missing_deps)}")
        print("请运行: pip install PyQt5 ultralytics opencv-python matplotlib numpy Pillow")
        print("\n是否继续? (y/n)")
        choice = input().strip().lower()
        if choice != 'y':
            return
    
    # 启动GUI
    print("\n🚀 启动轻量版系统...")
    print("💡 提示: 首次运行可能较慢，请耐心等待")
    print("=" * 50)
    
    try:
        # 添加路径
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from src.gui.simple_gui import main as gui_main
        gui_main()
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        print("\n请检查:")
        print("1. 依赖是否安装完整")
        print("2. 模型文件是否存在")
        print("3. 虚拟环境是否正确激活")
        
        input("\n按Enter键退出...")

if __name__ == "__main__":
    main()