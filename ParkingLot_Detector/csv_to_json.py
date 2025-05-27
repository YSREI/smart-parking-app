# csv_to_json.py

import argparse
from utils.csv_utils import csv_to_parking_spots_json

def convert(args):
    """
    Convert a CSV file of parking spot coordinates into JSON format.
    
    """
    csv_to_parking_spots_json(args.csv_path, args.output_path)
    print(f" Generated {args.output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_path', required=True, help="Input CSV file path")
    parser.add_argument('--output_path', required=True, help="Output JSON file path")
    args = parser.parse_args()

    convert(args)
