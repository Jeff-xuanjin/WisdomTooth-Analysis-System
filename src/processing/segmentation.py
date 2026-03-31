#!/usr/bin/env python3
"""
分割模块使用示例
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.processing.segmentation import DentalSegmentation
import cv2
import numpy as np

def main():
    """主函数"""
    print("🦷 牙齿分割模块使用示例")
    print("=" * 50)
    
    # 创建分割器
    segmentor = DentalSegmentation(conf_threshold=0.2, imgsz=320)
    
    # 创建测试图像
    print("🔧 创建测试图像...")
    test_image = np.zeros((400, 400, 3), dtype=np.uint8)
    test_image[:] = (200, 200, 200)  # 灰色背景
    
    # 创建几个模拟牙齿
    cv2.ellipse(test_image, (100, 150), (40, 60), 30, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(test_image, (200, 150), (35, 55), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(test_image, (300, 150), (45, 65), -30, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(test_image, (150, 250), (50, 70), 15, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(test_image, (250, 250), (40, 60), -15, 0, 360, (255, 255, 255), -1)
    
    # 创建模拟掩码和类别
    print("🔧 创建模拟数据...")
    masks = []
    class_ids = []
    
    # 牙齿1: 第二磨牙
    mask1 = np.zeros((400, 400), dtype=np.uint8)
    cv2.ellipse(mask1, (100, 150), (40, 60), 30, 0, 360, 255, -1)
    masks.append(mask1)
    class_ids.append(0)
    
    # 牙齿2: 第二磨牙
    mask2 = np.zeros((400, 400), dtype=np.uint8)
    cv2.ellipse(mask2, (200, 150), (35, 55), 0, 0, 360, 255, -1)
    masks.append(mask2)
    class_ids.append(0)
    
    # 牙齿3: 第三磨牙
    mask3 = np.zeros((400, 400), dtype=np.uint8)
    cv2.ellipse(mask3, (300, 150), (45, 65), -30, 0, 360, 255, -1)
    masks.append(mask3)
    class_ids.append(1)
    
    # 牙齿4: 第二磨牙
    mask4 = np.zeros((400, 400), dtype=np.uint8)
    cv2.ellipse(mask4, (150, 250), (50, 70), 15, 0, 360, 255, -1)
    masks.append(mask4)
    class_ids.append(0)
    
    # 牙齿5: 第三磨牙
    mask5 = np.zeros((400, 400), dtype=np.uint8)
    cv2.ellipse(mask5, (250, 250), (40, 60), -15, 0, 360, 255, -1)
    masks.append(mask5)
    class_ids.append(1)
    
    print(f"✅ 创建了 {len(masks)} 个模拟牙齿")
    
    # 计算统计
    print("📊 计算统计信息...")
    stats = segmentor.calculate_tooth_statistics(masks, class_ids)
    
    print(f"总牙齿数: {stats['total_teeth']}")
    for class_name, count in stats.get('by_class', {}).items():
        print(f"  {class_name}: {count}个")
    
    if 'area_stats' in stats:
        print(f"总面积: {stats['area_stats']['total']:,} 像素")
        print(f"平均面积: {stats['area_stats']['average']:.0f} 像素")
    
    # 创建可视化
    print("🎨 创建可视化...")
    vis_image = segmentor.create_visualization(test_image, masks, class_ids, stats)
    
    # 显示结果
    cv2.imshow("原始图像", test_image)
    cv2.imshow("分割结果", vis_image)
    
    print("👀 显示结果中... 按任意键关闭窗口")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # 生成报告
    print("📄 生成详细报告...")
    report = segmentor.create_detailed_report("test_dental_image.jpg", masks, class_ids, stats)
    
    print(f"报告包含 {len(report['detailed_analysis'])} 个牙齿的详细分析")
    for i, tooth in enumerate(report['detailed_analysis'][:3]):  # 显示前3个
        print(f"  牙齿 {tooth['id']}: {tooth['class_name']}, 面积: {tooth.get('area', 0)}像素")
    
    # 保存结果
    print("💾 保存结果...")
    output_dir = "./test_results"
    segmentor.save_results(output_dir, test_image, masks, class_ids, stats, report)
    
    print("\n✅ 示例完成！")
    print(f"结果保存在: {output_dir}")

if __name__ == "__main__":
    main()