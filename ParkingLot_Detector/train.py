#train.py
import argparse
from detector import ParkingLotDetector

def train(args):
    """
    entry point for training the parking lot detection model.

    """
    detector = ParkingLotDetector()
    detector.train(train_dir=args.train_dir, val_dir=args.val_dir, output_model_path=args.output_model_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir', required=True, help="Path to training dataset")
    parser.add_argument('--val_dir', required=True, help="Path to validation dataset")
    parser.add_argument('--output_model_path', required=True, help="Path to save the trained model")
    args = parser.parse_args()

    train(args)
