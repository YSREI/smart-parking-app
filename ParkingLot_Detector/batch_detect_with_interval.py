# batch_detect_with_interval.py
import argparse
import os
import glob
import json
import time
from detector import ParkingDetector
from utils.cloud_utils import CloudUploader

def batch_detect_with_interval(args):
    """
    detect parking space status from a batch of images with interval, result are uploaded to firebase
    """

    print(f"Loading model: {args.model_path}")
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

    image_files.sort() 
    
    if not image_files:
        print(f" No images found in {args.source_dir}")
        return

    print(f"Starting batch detection, {len(image_files)} images,interval = {args.interval} seconds\n")

    for idx, image_path in enumerate(image_files):
        print(f"[{idx+1}/{len(image_files)}] Processing: {os.path.basename(image_path)}")
        output_path = os.path.join(args.output_dir, f"result_{os.path.basename(image_path)}")
        results = detector.detect_image(image_path, output_path)


        occupied_count = sum(1 for spot in results.values() if spot["status"] == "occupied")
        empty_count = sum(1 for spot in results.values() if spot["status"] == "empty")

        success = uploader.upload_parking_status(occupied_count, empty_count)
        if success:
            uploader.upload_spaces_status(results)
            print(f" {os.path.basename(image_path)} status successfully updated")
        else:
            print(f" Failed to upload {os.path.basename(image_path)} status")

        if idx != len(image_files) - 1:
            print(f"Waiting {args.interval} seconds...\n")
            time.sleep(args.interval)

    print("All images has been processed!")

    # In the future, if the user need to process license plate recognition, call the process_plate method of plate_recognise.py here
    # plate_number, confidence = recognizer.recognize_plate_number(image_path)
    # recognizer.process_plate(plate_number, confidence, image_name)
if __name__ == "__main__":
    class Args:
        model_path = "C:/Users/yushi/SmartParkingFinalProject/ParkingLot_Detector/model/parking_detector.pth"
        config_path = "C:/Users/yushi/SmartParkingFinalProject/ParkingLot_Detector/config/camera8_spots.json"
        source_dir = "C:/Users/yushi/SmartParkingFinalProject/ParkingLot_Detector/config/camera8_test_images/camera8"
        output_dir = "C:/Users/yushi/SmartParkingFinalProject/ParkingLot_Detector/output"
        api_url = "https://smartparkingapp-1d951-default-rtdb.europe-west1.firebasedatabase.app/"
        lot_id = "lot-c"
        interval = 10

    args = Args()
    batch_detect_with_interval(args)
