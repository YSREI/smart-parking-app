# Intelligent Parking Management System

An integrated smart parking solution combining Automatic Number Plate Recognition (ANPR), real-time parking slot detection, and a mobile application interface for users.



## Project Overview

This intelligent parking management system is designed to address the inefficiencies of traditional urban parking by combining:

- Real-time vehicle entry detection and plate recognition (ANPR).
- Parking slot availability detection using deep learning.
- A mobile app (React Native) for users to search, park, and pay.

The project focuses on real-world feasibility, edge device integration, Firebase-based cloud sync, and user experience optimisation.



## System Components

### 1. [Mobile App – React Native](https://github.com/YSREI/smart-parking-app)

- Real-time parking status display
- Plate-based entry/exit & fee calculation
- Firebase-based user login and history
- Simulated payment and log tracking

### 2. [ANPR Detector – YOLOv8 + Tesseract OCR](https://github.com/YSREI/ANPR_Detector)

- Vehicle detection using YOLOv8
- License plate cropping and recognition using Tesseract
- Frame-by-frame analysis on video input or image batches

### 3. [Parking Slot Detector – Hybrid-PLOD](https://github.com/YSREI/ParkingLot-Detector)

- Uses ResNet18 + LSTM hybrid model
- Perspective transformation for camera calibration
- Determines parking slot occupancy status in real-time



## My Roles and Contributions

- Designed and implemented the full mobile application in React Native
- Built and trained the parking slot classification model (ResNet18 + LSTM)
- Integrated YOLOv8 + OCR pipeline for accurate plate recognition
- Built end-to-end cloud sync pipeline via Firebase Realtime Database
- Designed system architecture and demo workflow
- Conducted final system testing and UI refinement



## Technologies Used

- YOLOv8, Tesseract OCR, OpenCV
- PyTorch (ResNet18)
- React Native, Expo, Firebase
- Python, JavaScript, Android Emulator



## Repo Structure

| Repo Name                                                    | Function                        |
| ------------------------------------------------------------ | ------------------------------- |
| [`smart-parking-app`](https://github.com/YSREI/smart-parking-app) | Mobile user app                 |
| [`ANPR_Detector`](https://github.com/YSREI/ANPR_Detector)    | Plate detection and recognition |
| [`ParkingLot-Detector`](https://github.com/YSREI/ParkingLot-Detector) | Parking space status detection  |
