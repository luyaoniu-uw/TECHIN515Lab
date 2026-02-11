"""Automated offloading evaluation test script.

Sends gesture feature vectors to the Flask /predict endpoint, records
predictions and latency, and simulates local inference results to produce
a dataset for analysis in offloading_evaluation.ipynb.

Usage:
    python test_offloading.py --server http://localhost:8000
    python test_offloading.py --server http://localhost:8000 --data-dir ../data
"""

import argparse
import csv
import os
import random
import time
from pathlib import Path
from typing import Optional

import numpy as np
import requests


def load_gesture_data(data_dir: str) -> list[tuple[str, list[float]]]:
    """Load gesture CSV files from subdirectories (one per class).

    Expected structure:
        data_dir/
            V/
                sample1.csv
                sample2.csv
            O/
                sample1.csv
            ...

    Each CSV has columns: timestamp, x, y, z (from Lab 4's process_gesture_data.py).
    Returns list of (label, feature_vector) tuples.
    """
    samples: list[tuple[str, list[float]]] = []
    data_path = Path(data_dir)

    if not data_path.exists():
        print(f"Warning: Data directory '{data_dir}' not found.")
        return samples

    for class_dir in sorted(data_path.iterdir()):
        if not class_dir.is_dir() or class_dir.name.startswith("."):
            continue

        label = class_dir.name
        csv_files = sorted(class_dir.glob("*.csv"))
        print(f"  Found {len(csv_files)} CSV files for class '{label}'")

        for csv_file in csv_files:
            try:
                data = np.loadtxt(csv_file, delimiter=",", skiprows=1)
                # Lab 4 CSVs have columns: timestamp, x, y, z
                # Extract x, y, z (columns 1-3), skip timestamp (column 0)
                feature_vector = data[:, 1:4].flatten().tolist()
                samples.append((label, feature_vector))
            except Exception as e:
                print(f"  Warning: Could not load {csv_file}: {e}")

    return samples


def generate_synthetic_data(
    gesture_labels: list[str],
    samples_per_class: int = 25,
    feature_size: int = 300,
) -> list[tuple[str, list[float]]]:
    """Generate synthetic test vectors as a fallback when real data is unavailable.

    Creates random feature vectors with slight per-class biases so that
    the cloud model produces varied confidence levels.
    """
    # Fixed per-class biases for reproducibility (hash() is non-deterministic in Python 3.3+)
    class_biases = {label: i * 0.05 for i, label in enumerate(gesture_labels)}

    samples: list[tuple[str, list[float]]] = []
    for label in gesture_labels:
        for _ in range(samples_per_class):
            bias = class_biases[label]
            vector = (np.random.randn(feature_size) * 0.5 + bias).tolist()
            samples.append((label, vector))
    return samples


def simulate_local_inference(
    cloud_gesture: str,
    cloud_confidence: float,
    true_label: str,
    gesture_labels: list[str],
) -> tuple[str, float]:
    """Simulate local (edge) inference results.

    Approximates a weaker edge model by adding noise to cloud predictions.
    This lets students analyze offloading tradeoffs even without real ESP32
    serial output. Students who capture real ESP32 data can replace these values.
    """
    # Local model is generally less confident
    local_confidence = max(0.0, cloud_confidence - random.uniform(5.0, 25.0))

    # Local model sometimes makes different predictions (error rate ~15%)
    if random.random() < 0.15:
        wrong_labels = [g for g in gesture_labels if g != cloud_gesture]
        local_gesture = random.choice(wrong_labels) if wrong_labels else cloud_gesture
    else:
        local_gesture = cloud_gesture

    return local_gesture, round(local_confidence, 2)


def query_server(
    server_url: str, feature_vector: list[float]
) -> Optional[dict]:
    """Send a feature vector to the Flask /predict endpoint."""
    url = f"{server_url.rstrip('/')}/predict"
    payload = {"data": feature_vector}
    try:
        start = time.time()
        response = requests.post(url, json=payload, timeout=10)
        latency_ms = round((time.time() - start) * 1000, 1)

        if response.status_code == 200:
            result = response.json()
            result["latency_ms"] = latency_ms
            return result
        else:
            print(f"  Server error {response.status_code}: {response.text[:100]}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"  Connection error: {e}")
        return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send gesture vectors to Flask server and log results"
    )
    parser.add_argument(
        "--server",
        default="http://localhost:8000",
        help="Flask server URL (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--data-dir",
        default=None,
        help="Path to gesture data directory (subdirectories per class with CSVs)",
    )
    parser.add_argument(
        "--output",
        default="offloading_results.csv",
        help="Output CSV path (default: offloading_results.csv)",
    )
    parser.add_argument(
        "--labels",
        nargs="+",
        default=["V", "O", "Z", "S"],
        help="Gesture labels (default: V O Z S)",
    )
    parser.add_argument(
        "--samples-per-class",
        type=int,
        default=25,
        help="Samples per class for synthetic data (default: 25)",
    )
    args = parser.parse_args()

    # Load or generate test data
    if args.data_dir:
        print(f"Loading gesture data from: {args.data_dir}")
        samples = load_gesture_data(args.data_dir)
        if not samples:
            print("No data found. Falling back to synthetic data.")
            samples = generate_synthetic_data(args.labels, args.samples_per_class)
    else:
        print("No --data-dir specified. Generating synthetic test data.")
        samples = generate_synthetic_data(args.labels, args.samples_per_class)

    print(f"Total samples: {len(samples)}")

    # Verify server is reachable
    try:
        resp = requests.get(args.server.rstrip("/") + "/", timeout=5)
        print(f"Server status: {resp.status_code} - {resp.text.strip()}")
    except requests.exceptions.RequestException as e:
        print(f"Cannot reach server at {args.server}: {e}")
        print("Make sure the Flask server is running (python app/app.py)")
        return

    # Run evaluation
    results: list[dict] = []
    for i, (true_label, feature_vector) in enumerate(samples):
        cloud_result = query_server(args.server, feature_vector)
        if cloud_result is None:
            continue

        cloud_gesture = cloud_result["gesture"]
        cloud_confidence = cloud_result["confidence"]
        cloud_latency = cloud_result["latency_ms"]

        # Simulate local inference
        local_gesture, local_confidence = simulate_local_inference(
            cloud_gesture, cloud_confidence, true_label, args.labels
        )
        # Simulate local latency (typically 5-30ms on ESP32)
        local_latency = round(random.uniform(5.0, 30.0), 1)

        results.append({
            "true_label": true_label,
            "local_prediction": local_gesture,
            "local_confidence": local_confidence,
            "local_latency_ms": local_latency,
            "cloud_prediction": cloud_gesture,
            "cloud_confidence": round(cloud_confidence, 2),
            "cloud_latency_ms": cloud_latency,
        })

        if (i + 1) % 20 == 0:
            print(f"  Processed {i + 1}/{len(samples)} samples...")

    # Write results
    if not results:
        print("No results collected. Check server connection.")
        return

    output_path = os.path.join(os.path.dirname(__file__) or ".", args.output)
    fieldnames = [
        "true_label",
        "local_prediction",
        "local_confidence",
        "local_latency_ms",
        "cloud_prediction",
        "cloud_confidence",
        "cloud_latency_ms",
    ]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to: {output_path}")
    print(f"Total records: {len(results)}")

    # Quick summary
    cloud_correct = sum(1 for r in results if r["cloud_prediction"] == r["true_label"])
    local_correct = sum(1 for r in results if r["local_prediction"] == r["true_label"])
    avg_cloud_latency = np.mean([r["cloud_latency_ms"] for r in results])
    avg_local_latency = np.mean([r["local_latency_ms"] for r in results])

    print(f"\nQuick Summary:")
    print(f"  Cloud accuracy:  {cloud_correct}/{len(results)} ({cloud_correct/len(results)*100:.1f}%)")
    print(f"  Local accuracy:  {local_correct}/{len(results)} ({local_correct/len(results)*100:.1f}%)")
    print(f"  Avg cloud latency: {avg_cloud_latency:.1f} ms")
    print(f"  Avg local latency: {avg_local_latency:.1f} ms")


if __name__ == "__main__":
    main()
