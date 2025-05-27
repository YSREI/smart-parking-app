import json

# 读取旧版camera8_spots.json
with open("C:/Users/yushi/SmartParkingFinalProject/ParkingLot_Detector/config/camera8_spots.json", "r") as f:
    old_data = json.load(f)

# 转换格式
new_data = []
for spot_id, coords in old_data.items():
    new_data.append({
        "id": str(spot_id),
        "coords": coords
    })

# 保存新文件
with open("C:/Users/yushi/SmartParkingFinalProject/ParkingLot_Detector/config/camera8_spots_fixed.json", "w") as f:
    json.dump(new_data, f, indent=4)

print("✅ camera8_spots.json 转换完成，输出到 camera8_spots_fixed.json！")
