# annotate.py
import argparse
import cv2
import json
import os

# Global variables
parking_spots = {}
current_spot = []
spot_id = 0

def mouse_callback(event, x, y, flags, param):
    """
    handle mouse click to record parking spot corners
    """
    global current_spot, spot_id
    if event == cv2.EVENT_LBUTTONDOWN:
        current_spot.append((x, y))
        print(f" Point ({x}, {y}) recorded")
        if len(current_spot) == 4:
            parking_spots[str(spot_id)] = {"points": current_spot}
            print(f"Spot {spot_id} saved")
            current_spot = []
            spot_id += 1

def annotate_parking_spots(image_path, output_json_path):
    """
    mouse click manully to record parking spot corners.
    """
    global parking_spots, current_spot, spot_id
    parking_spots = {}
    current_spot = []
    spot_id = 0

    img = cv2.imread(image_path)
    if img is None:
        print(f" Failed to read image {image_path}")
        return

    cv2.namedWindow("Annotate Parking Spots", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Annotate Parking Spots", mouse_callback)

    while True:
        cv2.imshow("Annotate Parking Spots", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # press q to save and quit
            break

    cv2.destroyAllWindows()

    # 保存JSON
    with open(output_json_path, 'w') as f:
        json.dump(parking_spots, f, indent=4)
    print(f"Annotations saved to {output_json_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', required=True, help="要Path to the image")
    parser.add_argument('--output_path', required=True, help="Path to save spot JSON")
    args = parser.parse_args()

    annotate_parking_spots(args.image_path, args.output_path)
