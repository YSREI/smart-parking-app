# create_ground_truth.py

import argparse
import cv2
import os
import json

def create_ground_truth(args):
    """
    Manually label parking space status by viewing each image one-by-one.
    """

    images = [img for img in os.listdir(args.image_dir) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(images)} images for labeling")

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for img_name in images:
        img_path = os.path.join(args.image_dir, img_name)
        img = cv2.imread(img_path)

        if img is None:
            print(f"Cannot read image {img_path}")
            continue

        print(f" Current image: {img_name}")
        print("Press SPACE = Occupied, 'e' = Empty, 'n' = Skip")

        status = None
        while True:
            cv2.imshow('Label Image', img)
            key = cv2.waitKey(0) & 0xFF
            if key == ord(' '):
                status = 'occupied'
                break
            elif key == ord('e'):
                status = 'empty'
                break
            elif key == ord('n'):
                status = 'unknown'
                break

        cv2.destroyAllWindows()

        label_data = {
            "image": img_name,
            "status": status
        }

        output_path = os.path.join(args.output_dir, img_name.replace('.jpg', '.json'))
        with open(output_path, 'w') as f:
            json.dump(label_data, f, indent=4)

        print(f"Saved label: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', required=True, help="Folder with images to labe")
    parser.add_argument('--output_dir', required=True, help="Folder to save label JSON files")
    args = parser.parse_args()

    create_ground_truth(args)
