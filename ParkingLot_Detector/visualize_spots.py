# visualize_spots.py
import argparse
import cv2
import json
import os

def draw_spots(image_path, config_path):
    """
    Draw parking spot boundaries on an image using a JSON config file.

    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to read image: {image_path}")
        return

    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        return

    with open(config_path, 'r') as f:
        spots = json.load(f)

    for spot_id, data in spots.items():
        points = data["points"]
        pts = [(int(x), int(y)) for x, y in points]
        for i in range(4):
            cv2.line(image, pts[i], pts[(i + 1) % 4], (0, 255, 0), 2)
        x, y = pts[0]
        cv2.putText(image, f"{spot_id}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    cv2.imshow("Parking Spot Visualisation", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', required=True, help="Path to the image")
    parser.add_argument('--config_path', required=True, help="Path to JSON spot config")
    args = parser.parse_args()

    draw_spots(args.image_path, args.config_path)