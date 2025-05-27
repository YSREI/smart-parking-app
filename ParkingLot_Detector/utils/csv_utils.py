import pandas as pd
import json
import os
import cv2
import numpy as np


def convert_camera_csv_to_config(csv_path, config_path, scale_x=0.3858, scale_y=0.3858):
    """将摄像头CSV文件中的坐标转换为配置文件，并应用缩放比例"""
    import pandas as pd
    import json
    import os

    # 读取CSV文件
    df = pd.read_csv(csv_path)

    # 创建停车位配置列表
    parking_spots = []

    # 遍历每行数据
    for index, row in df.iterrows():
        # 应用缩放比例
        x = int(row['X'] * scale_x)
        y = int(row['Y'] * scale_y)
        w = int(row['W'] * scale_x)
        h = int(row['H'] * scale_y)

        # 将矩形坐标转换为四个角点坐标
        coords = [
            [x, y],  # 左上
            [x + w, y],  # 右上
            [x + w, y + h],  # 右下
            [x, y + h]  # 左下
        ]

        spot_id = str(row['SlotId'])

        parking_spots.append({
            "id": spot_id,
            "coords": coords
        })

    # 保存为JSON配置文件
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(parking_spots, f, indent=4)

    print(f"已转换并缩放{len(parking_spots)}个停车位配置到: {config_path}")
    return parking_spots


def visualize_spots_from_csv(csv_path, image_path, output_path, original_width=1000, original_height=750):
    """可视化CSV中的停车位坐标"""
    if not os.path.exists(csv_path):
        print(f"错误：CSV文件不存在: {csv_path}")
        return

    if not os.path.exists(image_path):
        print(f"错误：图像文件不存在: {image_path}")
        return

    # 读取CSV和图像
    df = pd.read_csv(csv_path)
    image = cv2.imread(image_path)
    if image is None:
        print(f"错误：无法读取图像: {image_path}")
        return

    # 复制图像用于绘制
    result = image.copy()

    # 绘制停车位
    for index, row in df.iterrows():
        x, y, w, h = row['X'], row['Y'], row['W'], row['H']

        # 确保坐标在有效范围内
        if x < 0 or y < 0 or x + w > original_width or y + h > original_height:
            print(f"警告：停车位 {row['SlotId']} 坐标超出图像范围: ({x},{y},{w},{h})")
            continue

        # 绘制矩形和ID
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(result, str(row['SlotId']), (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 保存结果
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, result)
    print(f"已保存可视化结果到: {output_path}")