# evaluate_model.py
import argparse
from detector import ParkingLotDetector

def evaluate(args):
    """
    evaluate the model
    """
    detector = ParkingLotDetector(args.model_path)
    accuracy = detector.evaluate(val_dir=args.val_dir)
    print(f" Model accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', required=True, help="Path to trained model file")
    parser.add_argument('--val_dir', required=True, help="Path to validation dataset")
    args = parser.parse_args()

    evaluate(args)
