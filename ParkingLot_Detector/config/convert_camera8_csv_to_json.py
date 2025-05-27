import pandas as pd
import json

# 读取csv
csv_file = "camera8.csv"
df = pd.read_csv(csv_file)

# 定义缩放比例
scale_x = 0.3858
scale_y = 0.3858

# 构建字典
spots = {}

for idx, row in df.iterrows():
    slot_id = str(int(row['SlotId']))  # ← ← ← ← 注意是 SlotId
    x, y, w, h = row['X'], row['Y'], row['W'], row['H']

    spots[slot_id] = [
        [int(x * scale_x), int(y * scale_y)],
        [int((x + w) * scale_x), int(y * scale_y)],
        [int((x + w) * scale_x), int((y + h) * scale_y)],
        [int(x * scale_x), int((y + h) * scale_y)]
    ]

# 保存为json
with open("camera8_spots.json", "w") as f:
    json.dump(spots, f, indent=4)

print(f"✅ Successfully converted {len(spots)} parking spots to camera8_spots.json with scaling and 4-point conversion!")
