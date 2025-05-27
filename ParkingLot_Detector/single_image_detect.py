# single_image_detector.py

import argparse
from detector import ParkingLotDetector

def detect_single(args):
    """
    detect parking spots from a single image.

    """
    detector = ParkingLotDetector(args.model_path)
    if not detector.load_parking_spots(args.config_path):
        print("Failed to load parking spot configuration.")
        return

    detector.detect_image(args.image_path, args.output_path)
    print(f" Detection complete. Result saved to {args.output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', required=True, help="Path to trained model")
    parser.add_argument('--config_path', required=True, help="Path to parking spots config JSON")
    parser.add_argument('--image_path', required=True, help="Path to the input image")
    parser.add_argument('--output_path', required=True, help="Path to save the output image")
    args = parser.parse_args()

    detect_single(args)
