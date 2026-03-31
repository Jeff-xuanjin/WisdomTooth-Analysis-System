#!/usr/bin/env python3
"""
环境诊断工具
检查当前Python环境配置
"""

import sys
import os
import subprocess
import json
from pathlib import Path

def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 60)
    print(f"📊 {title}")
    print("=" * 60)

def main():
    """主函数"""
    print("🦷 牙齿分割系统环境诊断工具")
    print("=" * 60)
    
    # 1. Python 信息
    print_section("Python 信息")
    print(f"Python 版本: {sys.version}")
    print(f"Python 路径: {sys.executable}")
    print(f"虚拟环境路径: {sys.prefix}")
    
    # 2. 环境变量
    print_section("环境变量")
    path = os.environ.get('PATH', '').split(';')
    python_paths = [p for p in path if 'python' in p.lower() or 'conda' in p.lower()]
    print("PATH 中的 Python 相关路径:")
    for i, p in enumerate(python_paths[:10], 1):
        print(f"  {i:2d}. {p}")
    if len(python_paths) > 10:
        print(f"  ... 还有 {len(python_paths)-10} 个路径未显示")
    
    # 3. Conda 信息
    print_section("Conda 信息")
    try:
        result = subprocess.run(['conda', 'info', '--envs'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("所有 conda 环境:")
            print(result.stdout)
        else:
            print("无法获取 conda 信息")
    except Exception as e:
        print(f"获取 conda 信息失败: {e}")
    
    # 4. 当前环境变量
    print_section("当前环境")
    env_vars = ['CONDA_DEFAULT_ENV', 'CONDA_PREFIX', 'CONDA_EXE', 'PYTHONPATH']
    for var in env_vars:
        value = os.environ.get(var, '未设置')
        print(f"{var}: {value}")
    
    # 5. 项目结构
    print_section("项目结构")
    project_root = Path(__file__).parent
    print(f"项目根目录: {project_root}")
    
    required_files = [
        ("simple_main.py", "主程序"),
        ("src/__init__.py", "包初始化"),
        ("src/core/teeth_segmentor.py", "分割器"),
        ("src/visualization/plotter.py", "可视化器"),
        ("src/gui/simple_gui.py", "GUI界面"),
        ("models/weights/best.pt", "模型文件")
    ]
    
    for file_path, description in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            if file_path.endswith('.pt'):
                size_mb = full_path.stat().st_size / (1024 * 1024)
                print(f"✅ {description}: {file_path} ({size_mb:.1f}MB)")
            else:
                print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (缺失)")
    
    # 6. VS Code 配置
    print_section("VS Code 配置")
    vscode_settings = project_root / ".vscode" / "settings.json"
    if vscode_settings.exists():
        print(f"找到 .vscode/settings.json")
        try:
            with open(vscode_settings, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                python_path = settings.get('python.defaultInterpreterPath', '未设置')
                print(f"Python 解释器路径: {python_path}")
        except:
            print("无法读取 settings.json")
    else:
        print("未找到 .vscode/settings.json")
    
    # 7. 依赖检查
    print_section("依赖检查")
    dependencies = [
        ('PyQt5', 'GUI界面'),
        ('ultralytics', 'YOLO模型'),
        ('cv2', 'OpenCV'),
        ('matplotlib', '可视化'),
        ('numpy', '数值计算'),
        ('PIL', '图像处理')
    ]
    
    for module, description in dependencies:
        try:
            if module == 'cv2':
                import cv2
                version = cv2.__version__
            elif module == 'PIL':
                from PIL import Image
                version = Image.__version__
            else:
                mod = __import__(module)
                version = getattr(mod, '__version__', '未知版本')
            print(f"✅ {description} ({module}): {version}")
        except ImportError:
            print(f"❌ {description} ({module}): 未安装")
    
    # 8. 建议
    print_section("诊断建议")
    python_exe = str(sys.executable)
    
    if 'dental_software' in python_exe and '3.8' in sys.version:
        print("✅ 环境配置正确！")
        print(f"   当前使用 dental_software 虚拟环境")
        print(f"   Python 版本: 3.8.x")
    elif 'dental_software' not in python_exe:
        print("⚠️  未使用 dental_software 虚拟环境")
        print("   建议在 VS Code 中:")
        print("   1. 按 Ctrl+Shift+P")
        print("   2. 输入 'Python: Select Interpreter'")
        print("   3. 选择 'dental_software' 环境")
    elif '3.8' not in sys.version:
        print("⚠️  Python 版本不是 3.8.x")
        print(f"   当前版本: {sys.version.split()[0]}")
    
    print("\n" + "=" * 60)
    print("🚀 运行系统: python simple_main.py")
    print("=" * 60)

if __name__ == "__main__":
    main()