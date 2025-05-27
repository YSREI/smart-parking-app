# SMART PARKING LOT DETECTOR

This is the backend implementation of a Smart Parking Management System that detects parking space occupancy from images or video frames using a deep learning model. The system supports model training, single/batch image detection, evaluation, annotation, and Firebase cloud upload.



## Project Structure

| File/Module                   | Description                                           |
| ----------------------------- | ----------------------------------------------------- |
| parking_detector.pth          | Trained model for parking lot detection.              |
| detector.py                   | Model definition and detection class.                 |
| train.py                      | Train the model.                                      |
| evaluate_model.py             | Evaluate model accuracy.                              |
| single_image_detect.py        | Detect parking status from a single image.            |
| batch_detect.py               | Detect and upload results for all images in a folder. |
| batch_detect_with_interval.py | Timed upload simulation for demo purposes.            |
| annotate.py                   | Annotate parking spots manually.                      |
| visualize_spots.py            | Draw annotated spots on image.                        |
| create_ground_truth.py        | Manually label image occupancy for training.          |
| csv_to_json.py                | Convert spot data from CSV to JSON format.            |
| utils/                        | Additional scripts (e.g., cloud_utils, csv_utils).    |



---

## Setup Instructions

```bash
pip install -r requirements.txt
```



## How to Run

### 1. Train the Model
```bash
python train.py --train_dir data/train --val_dir data/val --output_model_path models/best_model.pth
```

### 2. Evaluate the Model
```bash
python evaluate_model.py --model_path models/best_model.pth --val_dir data/val
```

### 3. Detect from a Single Image
```bash
python single_image_detect.py --model_path models/best_model.pth \
  --config_path config/spots.json --image_path test.jpg --output_path output.jpg
```

### 4. Batch Detection + Upload to Firebase
```bash
python batch_detect.py --model_path models/best_model.pth \
  --config_path config/spots.json --source_dir input/ --output_dir output/ --lot_id lot-c
```

### 5. Simulate Real-Time Upload
```bash
python batch_detect_with_interval.py --model_path models/best_model.pth \
  --config_path config/spots.json --source_dir input/ --output_dir output/ --lot_id lot-c --interval 10
```

### 6. Annotate Parking Spots
```bash
python annotate.py --image_path image.jpg --output_path config/spots.json
```

### 7. Visualize Annotated Spots
```bash
python visualize_spots.py --image_path image.jpg --config_path config/spots.json
```

---



## Notes

- All image files should be `.jpg`, `.jpeg`, or `.png` format.
- Firebase credentials and URLs are set in `cloud_utils.py` or relevant files.
- The parking space coordinates provided in `camera8_spots.json` are annotated based on the original **image resolution of 2592×1944 pixels**. These coordinates represent the bounding boxes of each parking space in that resolution. So, to fit the 1000*750 size of the CNRPARK dataset, I scaled the coordinates down by an equal amount.
