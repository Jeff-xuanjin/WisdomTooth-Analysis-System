# WisdomTooth-Analysis-System
基于深度学习与计算机视觉的口腔曲面断层影像智能分析系统。自动分割下颌第二、第三磨牙，为临床医生提供直观的智齿位置关系分析，是可靠性与系统工程学院"春苗计划"科研训练项目成果。

📋 目录

🎯 项目简介

✨ 核心功能

🏗️ 技术架构

📁 项目结构

⚙️ 系统要求

🚀 快速开始

🖥️ 使用指南

🔬 技术细节

📄 许可证

🤝 如何贡献

📞 联系我们

⚠️ 免责声明

🎯 项目简介

智齿影像智能分析系统​ 是一款基于YOLOv8深度学习模型开发的桌面端软件，专门用于分析口腔曲面断层影像（全景片）中下颌第二磨牙与第三磨牙（智齿）的相对位置关系。该系统通过实例分割技术精准定位目标牙齿，为后续的定量参数分析（如倾斜角度、距离计算）提供基础，旨在辅助口腔科医生进行临床诊断与治疗规划。

本项目是北航可靠性与系统工程学院本科生"春苗计划"科研训练项目的成果，项目周期为2025年4月至2026年3月。

✨ 核心功能

智能牙齿分割

基于改进的YOLOv8-seg实例分割模型。

可同时高精度分割下颌第二磨牙与第三磨牙。

提供分割掩码与轮廓可视化。

影像可视化与交互

显示分割结果。

支持常见图片格式（PNG）。

直观的结果对比展示。

结果输出与保存

可保存分割结果图片。

记录检测到的牙齿数量与类别。

后续可扩展的参数分析框架

系统架构为自动化参数计算预留接口。

计划通过主成分分析拟合牙齿长轴，计算相对倾斜角度。

计划计算牙齿间中心点距离与最小轮廓距离。

🏗️ 技术架构

系统采用模块化设计，主要分为以下几个部分：

用户交互层 (GUI - PyQt5)

       
业务逻辑层 (图像处理、模型调度、参数计算)

       
深度学习层 (YOLOv8-seg 实例分割模型)

       
数据层 (本地影像文件、模型权重)

📁 项目结构

WisdomTooth-Analysis-System/   
TeethAnalysis/                      # 牙齿分割识别系统 - 主项目目录  
│  
├─ config/                          # 配置文件目录  
│  
├─ data/                            # 数据目录  
│  
├─ diagnose_env.py                  # 环境诊断脚本，检查Python环境  
├─ docs/                            # 项目文档目录  
├─ environment.yml                  # Conda环境配置文件  
├─ from PIL import Image.py         # 废弃的图片处理脚本（文件名有问题，应重命名）  
├─ logs/                            # 日志文件目录  
│  
├─ models/                          # 模型文件目录    
│  
├─ notebooks/                       # Jupyter Notebooks目录（用于实验和可视化）  
├─ project_structure.txt            # 项目结构说明文件  
├─ README.md                        # 项目主说明文档  
├─ requirements.txt                 # Python依赖包列表  
├─ resources/                       # 资源文件目录（如图标、字体等）  
├─ results/                         # 结果输出目录  
│  
├─ run.bat                          # Windows批处理启动脚本  
├─ simple_main.py                   # 系统主入口文件  
│  
├─ src/                             # 源代码目录  
│  ├─ analysis/                     # 数据分析模块目录  
│  ├─ core/                         # 核心算法模块  
│  │  
│  ├─ gui/                          # 图形用户界面模块  
│  │  
│  ├─ processing/                   # 图像处理模块  
│  │  └─ segmentation.py            # 分割处理核心类  
│  │  
│  ├─ utils/                        # 工具函数模块  
│  │  
│  └─visualization/                # 可视化模块  
│  
├─ test.jpg                         # 测试图片1  
├─ test.png                         # 测试图片2  
├─ tests/                           # 单元测试目录  
├─ test_launch.py                   # 启动测试脚本  
└─ zhiling                          # 虚拟环境强制更改指令  
⚙️ 系统要求  
操作系统：Windows 10/11, Ubuntu 18.04+, macOS 10.15+  
Python：3.8, 3.9, 3.10, 3.11  
内存：≥4GB RAM  
存储：≥2GB可用空间  
显卡：支持CUDA的NVIDIA GPU（可选，可加速），但已针对CPU进行优化  
🚀 快速开始  
1. 克隆仓库  
git clone https://github.com/Jeff-xuanjin/WisdomTooth-Analysis-System.git
cd WisdomTooth-Analysis-System
2. 创建虚拟环境（推荐）  
conda create -n dental_software python=3.8.20
conda activate dental_software
或  
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
3. 安装依赖  
pip install -r requirements.txt
requirements.txt应包含：ultralytics, torch, torchvision, opencv-python, numpy, matplotlib, pillow, PyQt5
4. 下载模型  
确保模型文件 best.pt位于 ./models/weights/目录下。如果不存在，请按项目说明获取。  
5. 运行程序  
python simple_main.py  
🖥️ 使用指南  
启动软件：运行 simple_main.py，将出现图形用户界面。  
加载影像：点击“选择牙片”按钮，从本地选择一张口腔曲面断层影像。  
执行分割：点击“分割识别”按钮，系统将自动运行模型，分割下颌第二、第三磨牙。  
查看结果：右侧窗口将显示分割结果，左侧为原图。状态栏会显示检测到的牙齿数量。  
保存结果：点击“保存结果”按钮，可将分析结果图片保存至本地。  
🔬 技术细节  
深度学习模型  
基础网络：YOLOv8-seg，一种先进的实例分割架构。  
训练数据：使用近400张标注的口腔曲面断层影像。  
优化目标：专注于下颌第二、第三磨牙的分割精度。  
部署：模型经过优化，可在CPU上高效运行，满足临床环境部署需求。  
关键算法（计划实现）  
牙齿长轴拟合：采用主成分分析对分割出的牙齿掩码像素点进行拟合，以确定其长轴方向[8]。该方法相比基于关键点的方法更具鲁棒性。  
相对角度计算：通过计算第二磨牙与第三磨牙长轴方向向量之间的夹角，得到智齿的倾斜角度。  
距离测量：计算两牙质心间的欧氏距离，以及轮廓间的最小距离，以评估空间关系。  
📄 许可证  
本项目采用 MIT 许可证。  
🤝 如何贡献  
我们欢迎任何形式的贡献，包括但不限于：  
报告Bug或提出新功能建议  
改进代码或文档  
分享使用经验或案例  
请通过GitHub的Issue和Pull Request功能进行协作。  
📞 联系我们  
如有任何问题或合作意向，请通过以下方式联系：  
项目负责人：[张杰夫]  
电子邮箱：2594252262@qq.com  
项目地址：  
⚠️ 免责声明  
本软件为科研训练项目成果，仅供学术研究参考，不用于临床诊断。  
本系统旨在辅助分析，不能替代专业医生的诊断。  
开发者不对因使用本软件而导致的任何直接或间接损失负责。  
用户在使用本软件处理患者影像前，应确保已获得必要的伦理批准和患者知情同意。  
如果此项目对您有帮助，请考虑给它点个Star！⭐  
