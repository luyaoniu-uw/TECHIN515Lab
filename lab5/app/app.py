from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np

app = Flask(__name__)

# Load model once at startup
model = load_model("wand_model.h5")

# IMPORTANT: Update this list to match the gesture classes your model was
# trained on, in the same order used during training. For example, if you
# trained with ["O", "V"], use ["O", "V"] here — not ["V", "O", "Z", "S"].
gesture_labels = ["V", "O", "Z", "S"]

# Expected feature vector length (must match model input shape)
EXPECTED_FEATURE_SIZE = model.input_shape[1]


@app.route("/", methods=["GET"])
def home():
    return "Wand Gesture API is running!"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json.get("data")
        if not data:
            raise ValueError("Missing 'data' field")

        if len(data) != EXPECTED_FEATURE_SIZE:
            raise ValueError(
                f"Expected {EXPECTED_FEATURE_SIZE} features, got {len(data)}"
            )

        input_array = np.array(data).reshape(1, -1)
        prediction = model.predict(input_array)

        top_index = int(np.argmax(prediction))
        label = gesture_labels[top_index]
        confidence = float(prediction[0][top_index]) * 100

        return jsonify({
            "gesture": label,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
