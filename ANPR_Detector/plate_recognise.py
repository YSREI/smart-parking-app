
# plate_recognise.py
# License Plate Recognition Module for Smart Parking System
# Author: Yu Shi
"""
This module performs automatic license plate detection and recognition using YOLOv8 for plate localisation and Tesseract OCR for text recognition.
It integrates with Firebase Realtime Database to manage parking entry/exit sessions.

Main capabilities:
- Process static image folders, video files, or live webcam streams.
- Extract license plates, recognise plate numbers, and upload results to Firebase.
- Prevent duplicate entry records and calculate parking charges upon exit.

"""
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import cv2
import numpy as np
from ultralytics import YOLO
import pytesseract
from datetime import datetime
import logging
import json
import firebase_admin
from firebase_admin import credentials, db
import time

# Set the Tesseract OCR path
TESSERACT_PATH = os.path.join(os.path.dirname(__file__), 'tesseract', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# initiate Firebase admin with credentials and URL
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smartparkingapp-1d951-default-rtdb.europe-west1.firebasedatabase.app/'
    })

def preprocess_plate_image(plate_img):
    """
    preprocess number plate image for better OCR accuracy

    - Convert to grayscale
    - Apply adaptive thresholding
    - Denoise
    - Enhance contrast using CLAHE
    """
    
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

    
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    denoised = cv2.fastNlMeansDenoising(binary)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    return enhanced


class LicensePlateRecognizer:
    def __init__(self, model_path, output_dir='detected_plates'):
        self.conf_threshold = 0.3
        """
        Initialise License Plate Recognition System

        - load YOLOv8 model for plate detection
        - configures logging and output folders
        - set up Tesseract OCR
        """
        self.setup_logging()

        self.model = YOLO(model_path)
        logging.info(f"Model loaded: {model_path}")

        self.output_dir = output_dir
        self.create_output_directories()
        self.setup_ocr()
        
        self.processed_plates = {}
        self.last_detection_time = time.time()


    def setup_logging(self):
        """
        Configuring the log system to file and console
        - track errors and performance
        """
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(
                    os.path.join(log_dir, f'plate_recognition_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')),
                logging.StreamHandler()
            ]
        )

    def create_output_directories(self):
        """
        Create directories for saving plate images and result json files
        """
        self.plate_images_dir = os.path.join(self.output_dir, 'plate_images')
        self.results_dir = os.path.join(self.output_dir, 'results')

        for directory in [self.plate_images_dir, self.results_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logging.info(f"Create Directories: {directory}")


    def setup_ocr(self):
        """
        Set up OCR engine with Tesseract
        - expects 1 line alphanumeric plates
        """
        self.ocr_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

        try:
            pytesseract.get_tesseract_version()
            logging.info("Tesseract OCR initialisation successful")
        except Exception as e:
            logging.error(f"Tesseract OCR initialisation failed: {str(e)}")
            raise

    def recognize_plate_number(self, plate_img):
        """
        run OCR on the cropped license plate image to extract plate number
        - applies preprocessing 
        - use tesseract OCR with strict alphanumeric whitelist
        - post-processing of text to filter out invalid results
        returns platen number string if valid, else none
        """
        processed_img = preprocess_plate_image(plate_img)

        try:
            plate_text = pytesseract.image_to_string(
                processed_img,
                config=self.ocr_config
            ).strip()

            plate_text = ''.join(c for c in plate_text if c.isalnum())
            if len(plate_text) >= 5:  
                return plate_text
            else:
                return None

        except Exception as e:
            logging.error(f"OCR failed: {str(e)}")
            return None
    
    def is_registered_user(self, plate_number):
        """
        Check in Firebase if this plate number belongs to a registered user.
        look under `users` node and compares against all license_plates fields.
        returns True if matched, else false.
        """
        try:
            users_ref = db.reference('users')
            users_snapshot = users_ref.get()

            if not users_snapshot:
                return False

            for user_id, user_data in users_snapshot.items():
                license_plates = user_data.get('license_plates', [])
                if plate_number in license_plates:
                    return True

            return False

        except Exception as e:
            logging.error(f"Error checking registration status: {str(e)}")
            return False


    def verify_and_register_entry(self, plate_number, confidence, image_name):
        """
        vehicle entry logic
        - if the user is registered and has no active session, create a new one
        - if unregistered, record in `unregistered-entries`(ideally this won't happen, I expect all the users registered before enter the car park)
        aviod dublicate entry for already parked vehicles.
        """
        normalized_plate = plate_number.replace(' ', '').upper()
        
        if not self.is_registered_user(normalized_plate):
            logging.warning(f"Plate {plate_number} is not registered")

            unregistered_ref = db.reference(f"unregistered-entries/{normalized_plate}")
            unregistered_ref.push({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "confidence": float(confidence)
            })
            return False
            
        sessions_ref = db.reference(f"parking-records/{normalized_plate}")
        sessions = sessions_ref.get()
        
        if sessions and isinstance(sessions, dict):
            for session_id, session_data in sessions.items():
                if session_data.get('paid') == False:
                    logging.info(f"Plate {plate_number} already has an active session")
                    return False
        
        now = datetime.now()
        entry_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        new_session_ref = sessions_ref.push()
        new_session_ref.set({
            "entryTime": entry_time,
            "paid": False,
            "entryMethod": "camera",
            "confidence": float(confidence),
            "image": image_name
        })
        
        logging.info(f"Created new entry session for {plate_number} at: {entry_time}")
        return True

    def verify_and_register_exit(self, plate_number, confidence, image_name):
        """
        vehicle exit logic
        - searches for active unpaid sessions
        - computes duration and fee (free ≤10min (just in case if no parking space can be found), £2/hr, capped at £10)
        - updates Firebase session as completed
        
        """
        try:
            normalized_plate = plate_number.replace(' ', '').upper()
            records_ref = db.reference(f'parking-records/{normalized_plate}')
            records_snapshot = records_ref.get()

            if not records_snapshot:
                logging.info(f"No session found for plate {plate_number} ")
                return False

            for session_id, session_data in records_snapshot.items():
                if session_data.get('paid') == False and session_data.get('exitTime') is None:
                    now = datetime.now()
                    exit_time = now.strftime("%Y-%m-%d %H:%M:%S")

                    entry_time_str = session_data.get('entryTime')
                    entry_time = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")

                    duration_minutes = (now - entry_time).total_seconds() / 60.0

                    if duration_minutes <= 10:
                        amount_due = 0.0
                    else:
                        hours = int(duration_minutes / 60) + (1 if duration_minutes % 60 > 0 else 0)
                        amount_due = hours * 2.0
                        if amount_due > 10.0:
                            amount_due = 10.0

                    session_ref = records_ref.child(session_id)
                    session_ref.update({
                        "exitTime": exit_time,
                        "durationMinutes": round(duration_minutes, 1),
                        "amountDue": round(amount_due, 2),
                        "exitConfidence": float(confidence),
                        "exitImage": image_name,
                        "paid": True 
                    })

                    logging.info(f"{plate_number} exited, {duration_minutes:.1f} mintues, charged £{amount_due:.2f}")
                    return True

            logging.info(f"No active session found for{plate_number}")
            return False

        except Exception as e:
            logging.error(f"Error processing exit for plate {plate_number} : {str(e)}")
            return False

    def process_plate(self, plate_number, confidence, image_name):
        """
        determine if the plate is entering or exiting
        - if the status is unpaid, ongoing session exits turns out to be an exit
        else treat as now entry
        """
        normalized_plate = plate_number.replace(' ', '').upper()
        records_ref = db.reference(f'parking-records/{normalized_plate}')
        records_snapshot = records_ref.get()

        has_active_session = False

        if records_snapshot and isinstance(records_snapshot, dict):
            for session_id, session_data in records_snapshot.items():
                if session_data.get('paid') == False and session_data.get('exitTime') is None:
                    has_active_session = True
                    break

        if has_active_session:
            return self.verify_and_register_exit(normalized_plate, confidence, image_name)
        else:
            return self.verify_and_register_entry(normalized_plate, confidence, image_name)


    def save_results(self, image_name, plate_img, plate_number, confidence):
        """
        save license plate images and recognition result
        also trigger entry/ exit logic.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if plate_number:
            image_filename = f"{plate_number}_{timestamp}.jpg"
        else:
            image_filename = f"unknown_{timestamp}.jpg"

        image_path = os.path.join(self.plate_images_dir, image_filename)
        cv2.imwrite(image_path, plate_img)

        result = {
            "original_image": image_name,
            "timestamp": timestamp,
            "plate_number": plate_number,
            "confidence": float(confidence),
            "plate_image_path": image_path
        }

        result_path = os.path.join(
            self.results_dir,
            f"result_{timestamp}.json"
        )

        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        logging.info(f"Saved result: {result_path}")

        self.process_plate(plate_number, confidence, image_name)
        
        return result

    def process_image(self, image_path):
        """
        detect and recognise license plates from a single image
        - runs YOLOv8 model to locate plates
        - performs OCR on cropped areas
        - draws results and saves annotated image
        """
        image = cv2.imread(image_path)
        if image is None:
            logging.error(f"Failed to read image: {image_path}")
            return None

        image_name = os.path.basename(image_path)

        results = self.model(image)
        all_results = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])

                plate_img = image[y1:y2, x1:x2]
                plate_number = self.recognize_plate_number(plate_img)

                if plate_number:
                    # draw box and label on original image
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(image, plate_number, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    result = self.save_results(
                        image_name, plate_img, plate_number, confidence
                    )
                    all_results.append(result)

                    logging.info(f"Detected plate: {plate_number}, Confidence level: {confidence:.4f}")

        # save annotated image
        output_image_path = os.path.join(
            self.output_dir,
            f"annotated_{image_name}"
        )
        cv2.imwrite(output_image_path, image)

        return all_results

    def process_directory(self, input_dir):
        """
        process all images files at a time in a given directory
        summarise the results and store the summary JSON.
        """
        logging.info(f"Processing directory: {input_dir}")

        all_results = []
        image_files = [f for f in os.listdir(input_dir)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for image_file in image_files:
            image_path = os.path.join(input_dir, image_file)
            results = self.process_image(image_path)
            if results:
                all_results.extend(results)

        summary_path = os.path.join(
            self.results_dir,
            f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=4)

        logging.info(f"Finished processing {len(image_files)} images.")
        logging.info(f"Summary saved to: {summary_path}")

        return all_results
    
    def process_video(self, video_path=None, camera_id=0, use_camera=False, frame_interval=30):
        """
        process a video file or live camera
        - capture every N frames
        - runs plate detection and recognition
        ingores repeat detection on the same number plate within 30s window(looking for further enhancements)
        """
        logging.info("Starting video stream...")
        
        if use_camera:
            cap = cv2.VideoCapture(camera_id)
            source_name = f"Camera-{camera_id}"
            logging.info(f"Using camera ID: {camera_id}")
        else:
            if not video_path:
                logging.error("No video path provided")
                return
            cap = cv2.VideoCapture(video_path)
            source_name = os.path.basename(video_path)
            logging.info(f"Processing video file: {video_path}")
        
        if not cap.isOpened():
            logging.error("Failed to open video stream")
            return
        
        # used to record the number of frames
        frame_id = 0
        # used to store detected license plates to avoid duplication 
        detected_plates = {}
        # store the processing results
        all_results = []
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # processed every specified number of frames
                if frame_id % frame_interval == 0:
                    temp_frame_path = os.path.join(self.output_dir, f"frame_{frame_id}.jpg")
                    cv2.imwrite(temp_frame_path, frame)
                    
                    results = self.model(frame, verbose=False)
                    for result in results:
                        boxes = result.boxes
                        for box in boxes:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            confidence = float(box.conf[0])
                            
                            plate_img = frame[y1:y2, x1:x2]
                            plate_number = self.recognize_plate_number(plate_img)
                            
                            if plate_number:
                                current_time = time.time()
                                if plate_number in detected_plates:
                                    last_time = detected_plates[plate_number]
                                    if current_time - last_time < 30:
                                        continue
                                
                                detected_plates[plate_number] = current_time
                                
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, plate_number, (x1, y1 - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                                
                                image_name = f"frame_{frame_id}.jpg"
                                result = self.save_results(
                                    image_name, plate_img, plate_number, confidence
                                )
                                all_results.append(result)
                    
                    # optional: add frame count overlay
                    cv2.putText(frame, f"Frame: {frame_id}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                
                frame_id += 1
                
                # 每处理100帧输出一条日志
                if frame_id % 100 == 0:
                    logging.info(f"Processed {frame_id} frames")
        
        except Exception as e:
            logging.error(f"Video processing error: {str(e)}")
        finally:
            cap.release()
        
        if all_results:
            summary_path = os.path.join(
                self.results_dir,
                f"video_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, ensure_ascii=False, indent=4)
            
            logging.info(f"Video finished, {len(all_results)} plates detected.")
            logging.info(f"Summary saved to: {summary_path}")
        else:
            logging.info("视Video finished, no plates detected.")
        
        return all_results


def main():
    """
    console entry point of the recogniser, offering 3 options
    - process a folder of images
    - process a video file
    - run live camera recognition
    """
    model_path = "./best.pt"
    output_dir = "./recognition"
    recognizer = LicensePlateRecognizer(model_path, output_dir)

    print("\n===== License Plate Recognition System =====")
    print("1. Process image directory")
    print("2. Process video file")
    print("3. Use live camera")
    choice = input("\nChoose mode (1/2/3): ")

    try:
        if choice == "1":
            input_dir = input("Enter image folder path [default: test_images]: ") or "test_images"
            if not os.path.exists(input_dir):
                print(f"Error: directory does not exist '{input_dir}'")
                return
            results = recognizer.process_directory(input_dir)
            print(f"\nRecognised {len(results)} plates.")
        
        elif choice == "2":
            video_path = input("Enter video file path: ")
            if not os.path.exists(video_path):
                print(f"Error: file does not exist '{video_path}'")
                return
            
            frame_interval = int(input("Enter frame interval [default: 20]: ") or "20")
            recognizer.process_video(video_path=video_path, frame_interval=frame_interval)
        
        # option 3 (live camera) is optional and requires a physical device
        #elif choice == "3":
        #    camera_id = int(input("Enter camera ID [default: 0]: ") or "0")
        #    frame_interval = int(input("Enter frame interval [default: 30]: ") or "30")
        #    recognizer.process_video(camera_id=camera_id, use_camera=True, frame_interval=frame_interval)
        #
        #    test_cap = cv2.VideoCapture(camera_id)
        #    if not test_cap.isOpened():
        #       print(f"Error: Camera ID {camera_id} is not available or accessible.")
        #        logging.warning(f"Camera ID {camera_id} could not be opened. Please check your device permissions.")
        #        test_cap.release()
        #        return
        #    test_cap.release()
        #
        #    recognizer.process_video(camera_id=camera_id, use_camera=True, frame_interval=frame_interval)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    except Exception as e:
        logging.error(f"Error during execution: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()