import argparse
import os
import glob
import json
from detector import ParkingDetector
from utils.cloud_utils import CloudUploader

def batch_detect(args):
    """
    Batch detect parking spaces from images in a folder and upload results to Firebase.
    
    """

    print(f"Loading model from: {args.model_path}")
    detector = ParkingDetector(args.model_path)
    if not detector.load_parking_spots(args.config_path):
        print(" Failed to load parking spot config.")
        return

    args.api_url = "https://smartparkingapp-1d951-default-rtdb.europe-west1.firebasedatabase.app/"

    uploader = CloudUploader(api_url=args.api_url, lot_id=args.lot_id)
    
    os.makedirs(args.output_dir, exist_ok=True)

    image_extensions = ['*.jpg', '*.jpeg', '*.png']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(args.source_dir, ext)))

    if not image_files:
        print(f"No images found in {args.source_dir}")
        return

    for idx, image_path in enumerate(image_files):
        print(f"Processing {idx+1}/{len(image_files)}: {os.path.basename(image_path)}")
        output_path = os.path.join(args.output_dir, f"result_{os.path.basename(image_path)}")
        results = detector.detect_image(image_path, output_path)

        occupied_count = sum(1 for spot in results.values() if spot["status"] == "occupied")
        empty_count = sum(1 for spot in results.values() if spot["status"] == "empty")

        success = uploader.upload_parking_status(occupied_count, empty_count)
        if success:
            print(f" {os.path.basename(image_path)} upload successful")

            uploader.upload_spaces_status(results)
        else:
            print(f" Failed to upload {os.path.basename(image_path)}")

    # In the future, if you also need to process license plate recognition, call the process_plate method of plate_recognise.py here
    # plate_number, confidence = recognizer.recognize_plate_number(image_path)
    # recognizer.process_plate(plate_number, confidence, image_name)

if __name__ == "__main__":
    class Args:
        model_path = "C:/Users/yushi/SmartParkingFinalProject/ParkingLot_Detector/model/parking_detector.pth"
        config_path = "C:/Users/yushi/SmartParkingFinalProject/ParkingLot_Detector/config/camera8_spots.json"
        source_dir = "C:/Users/yushi/SmartParkingFinalProject/ParkingLot_Detector/config/camera8_test_images"
        output_dir = "C:/Users/yushi/SmartParkingFinalProject/ParkingLot_Detector/output"
        api_url = "https://smartparkingapp-1d951-default-rtdb.europe-west1.firebasedatabase.app/"
        lot_id = "lot-c"

    args = Args()
    batch_detect(args)
