
# Smart Parking ANPR System

A modular Automatic Number Plate Recognition (ANPR) system designed for smart parking scenarios. This system uses YOLOv8 for plate detection, Tesseract OCR for character recognition, and Firebase for real-time data management.



## Project Structure

| File/Module            | Description |
|------------------------|-------------|
| run_plate_recognise.py | Main entry script. Set parameters inside the file to start image, video, or camera recognition. |
| recogniser.py         | Core class combining YOLO detection, OCR recognition, and Firebase result submission. |
| ocr_utils.py          | Handles plate image preprocessing and OCR logic using Tesseract. |
| firebase_utils.py    | Firebase interaction: check user registration, manage entry/exit sessions. |
| config.py             | Configuration for Firebase and OCR paths. |
| firebase_config.json  | Private Firebase Admin SDK key. |
| best.pt               | Trained YOLOv8 for license plate detection. |
| plate_recognise.py | Smart Parking License Plate Recognition (Single File Version), you can see a full comment in this module. |



## Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Make sure Tesseract is installed and  **tesseract.exe**  is placed in a  **tesseract/** folder at the project root menu.

### 2. Place config files

- **firebase_config.json**: Firebase credential JSON
- **best.pt**: YOLOv8 license plate detection model



## How to Run

Configure the parameters inside `run_plate_recognise.py`:

```python
if __name__ == "__main__":
    class Args:
        mode = "image"  # Options: image, video, camera
        input_dir = "./test_images"
        video_path = "./test_video.mp4"
        camera_id = 0
        frame_interval = 30
        model_path = "best.pt"
        output_dir = "recognition"
        
        
```

Run the system using:

```bash
python run_plate_recognise.py --input path/to/test_image.jpg --image
/ 
python plate_recognise.py
```
