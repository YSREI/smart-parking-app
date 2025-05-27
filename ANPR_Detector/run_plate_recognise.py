# run_plate_recognise.py
# Main entrypoint for Smart Parking ANPR System

import os
import cv2
from recogniser import LicensePlateRecognizer

def run_anpr(args):
    recogniser = LicensePlateRecognizer(model_path=args.model_path, output_dir=args.output_dir)

    if args.mode == "image":
        if not args.input_dir or not os.path.exists(args.input_dir):
            print(f"[ERROR] Invalid input_dir: {args.input_dir}")

            return
        
        results = recogniser.process_directory(args.input_dir)
        print(f"[DONE] Processed {len(results)} images.")

    elif args.mode == "video":
        if not args.video_path or not os.path.exists(args.video_path):
            print(f"[ERROR] Invalid video_path: {args.video_path}")

            return
        
        recogniser.process_video(video_path=args.video_path, frame_interval=args.frame_interval)

    elif args.mode == "camera":

        test_cap = cv2.VideoCapture(args.camera_id)
        if not test_cap.isOpened():
            print(f"[ERROR] Camera ID {args.camera_id} is not accessible.")
            return
        
        test_cap.release()
        recogniser.process_video(camera_id=args.camera_id, use_camera=True, frame_interval=args.frame_interval)

if __name__ == "__main__":
    class Args:
        mode = "image"                  # options: image / video / camera
        input_dir = "./test_images/images"    # used in image mode
        video_path = "./test_video.mp4"  # used in video mode
        camera_id = 0                  # used in camera mode
        frame_interval = 20            # frame skip interval
        model_path = "best.pt"         # path to YOLOv8 model
        output_dir = "recognition"     # output folder path

    args = Args()
    run_anpr(args)
