# recogniser.py
# LicensePlateRecognizer class includes detection, OCR, and Firebase handling

import os
import cv2
import json
import time
import logging
from datetime import datetime
from ultralytics import YOLO

from ocr_utils import recognize_plate_number
from firebase_utils import register_entry, register_exit
from config import *

class LicensePlateRecognizer:
    def __init__(self, model_path, output_dir="recognition"):
        self.model = YOLO(model_path)
        self.output_dir = output_dir
        self.plate_img_dir = os.path.join(output_dir, "plates")
        self.results_dir = os.path.join(output_dir, "results")
        os.makedirs(self.plate_img_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)
        self.setup_logging()

    def setup_logging(self):
        os.makedirs("logs", exist_ok=True)
        
        log_path = os.path.join("logs", f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",

            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler()
            ]
        )

    def save_results(self, image_name, plate_img, plate_number, confidence):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{plate_number}_{timestamp}.jpg" if plate_number else f"unknown_{timestamp}.jpg"
        image_path = os.path.join(self.plate_img_dir, image_filename)
        cv2.imwrite(image_path, plate_img)

        result = {
            "original_image": image_name,
            "timestamp": timestamp,
            "plate_number": plate_number,
            "confidence": float(confidence),
            "plate_image_path": image_path
        }

        result_path = os.path.join(self.results_dir, f"result_{timestamp}.json")
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        logging.info(f"Saved result: {result_path}")

        # Upload to Firebase
        if plate_number:
            plate = plate_number.replace(" ", "").upper()
            has_active_session = not register_exit(plate, confidence, image_name)

            if has_active_session:
                register_entry(plate, confidence, image_name)

        return result

    def process_image(self, image_path):
        image = cv2.imread(image_path)

        if image is None:
            logging.warning(f"Failed to load image: {image_path}")

            return []

        image_name = os.path.basename(image_path)
        results = self.model(image, verbose=False)
        output_results = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])

                plate_img = image[y1:y2, x1:x2]
                plate_number = recognize_plate_number(plate_img)

                if plate_number:

                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(image, plate_number, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    
                    result_data = self.save_results(image_name, plate_img, plate_number, confidence)
                    output_results.append(result_data)

        annotated_path = os.path.join(self.output_dir, f"annotated_{image_name}")
        cv2.imwrite(annotated_path, image)

        return output_results

    def process_directory(self, input_dir):
        all_results = []

        for fname in os.listdir(input_dir):
            if fname.lower().endswith((".jpg", ".jpeg", ".png")):

                fpath = os.path.join(input_dir, fname)
                results = self.process_image(fpath)
                all_results.extend(results)

        return all_results

    def process_video(self, video_path=None, camera_id=0, use_camera=False, frame_interval=30):
        if use_camera:
            cap = cv2.VideoCapture(camera_id)
        else:
            cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            logging.error("Failed to open video/camera stream.")

            return []

        frame_id = 0
        all_results = []

        while cap.isOpened():

            ret, frame = cap.read()
            if not ret:
                break

            if frame_id % frame_interval == 0:
                temp_path = os.path.join(self.output_dir, f"frame_{frame_id}.jpg")

                cv2.imwrite(temp_path, frame)

                results = self.process_image(temp_path)
                all_results.extend(results)

            frame_id += 1

        cap.release()
        return all_results
