import argparse
import json
import numpy as np
import requests


def main() -> None:
    parser = argparse.ArgumentParser(description="Test the Flask gesture prediction API")
    parser.add_argument(
        "--server",
        default="http://localhost:8000",
        help="Server URL (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--feature-size",
        type=int,
        default=300,
        help="Feature vector size (default: 300)",
    )
    args = parser.parse_args()

    url = f"{args.server.rstrip('/')}/predict"

    # Generate a random feature vector for testing
    dummy_data = np.random.rand(args.feature_size).tolist()
    print(f"Data shape: {len(dummy_data)}")

    # Build the JSON payload
    payload = {"data": dummy_data}

    # Send the POST request
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Handle response
    if response.status_code == 200:
        print("Prediction received:")
        print(response.json())
    else:
        print("Error:")
        print(f"Status code: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    main()
