@echo off
chcp 65001 >nul
title 🦷 牙齿分割系统 (轻量固定配置)
echo.
echo ==================================================
echo 🦷 牙齿分割识别系统
echo 固定轻量配置，适合轻薄笔记本
echo ==================================================
echo.

REM 激活虚拟环境
call conda activate dental_software

echo ✅ 虚拟环境激活
python --version
echo.

echo 📊 固定配置:
echo   分辨率: 320px
echo   置信度: 0.2
echo   设备: CPU
echo   半精度: 开启
echo   内存优化: 开启
echo.

echo 🔍 快速检查...
python -c "import sys; print('Python版本:', sys.version.split()[0])" 2>nul
if errorlevel 1 (
    echo ❌ Python错误
    pause
    exit /b 1
)

echo.
echo 🚀 启动系统...
echo 💡 提示: 首次运行可能较慢
echo      处理时请耐心等待
echo.

REM 运行主程序
python simple_main.py

echo.
echo ⏱️  处理完成！
pause