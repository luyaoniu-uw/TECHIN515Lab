/* Edge-Cloud Offloading Sketch
 * Based on Lab 4 wand.ino
 *
 * Performs local gesture inference on ESP32 using Edge Impulse.
 * When local confidence is below CONFIDENCE_THRESHOLD, offloads
 * raw sensor data to the Flask cloud server for inference.
 */

/* Includes ---------------------------------------------------------------- */
#include <test_wand_inferencing.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ==========================================================================
// TODO 1: Replace with your WiFi credentials and server URL
// ==========================================================================
const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* SERVER_URL    = "http://YOUR_SERVER_IP:8000/predict";

// Confidence threshold for offloading (0-100%)
#define CONFIDENCE_THRESHOLD 80.0

// MPU6050 sensor
Adafruit_MPU6050 mpu;

// Sampling and capture variables
#define SAMPLE_RATE_MS 10           // 100Hz sampling rate
#define CAPTURE_DURATION_MS 1000    // 1 second capture
#define FEATURE_SIZE EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE

// Capture state variables
bool capturing = false;
unsigned long last_sample_time = 0;
unsigned long capture_start_time = 0;
int sample_count = 0;

// Feature array to store accelerometer data
float features[FEATURE_SIZE];

/**
 * @brief      Copy raw feature data in out_ptr
 *             Function called by inference library
 */
int raw_feature_get_data(size_t offset, size_t length, float *out_ptr) {
    memcpy(out_ptr, features + offset, length * sizeof(float));
    return 0;
}

/**
 * @brief      Connect to WiFi network
 */
void connectWiFi() {
    Serial.print("Connecting to WiFi");
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 60) {
        delay(500);
        Serial.print(".");
        attempts++;
    }
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("\nFailed to connect to WiFi! Check credentials.");
        Serial.println("Continuing without WiFi (local inference only).");
        return;
    }
    Serial.println();
    Serial.print("Connected! IP address: ");
    Serial.println(WiFi.localIP());
}

/**
 * @brief      Arduino setup function
 */
void setup() {
    Serial.begin(115200);

    // Initialize WiFi
    connectWiFi();

    // Initialize MPU6050
    Serial.println("Initializing MPU6050...");
    if (!mpu.begin()) {
        Serial.println("Failed to find MPU6050 chip");
        while (1) {
            delay(10);
        }
    }

    // Configure MPU6050 — match settings with Lab 4 gesture_capture.ino
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

    Serial.println("MPU6050 initialized successfully");
    Serial.println("Send 'o' to start gesture capture");
}

/**
 * @brief      Capture accelerometer data for inference
 */
void capture_accelerometer_data() {
    if (millis() - last_sample_time >= SAMPLE_RATE_MS) {
        last_sample_time = millis();

        sensors_event_t a, g, temp;
        mpu.getEvent(&a, &g, &temp);

        if (sample_count < FEATURE_SIZE / 3) {
            int idx = sample_count * 3;
            features[idx]     = a.acceleration.x;
            features[idx + 1] = a.acceleration.y;
            features[idx + 2] = a.acceleration.z;
            sample_count++;
        }

        if (millis() - capture_start_time >= CAPTURE_DURATION_MS) {
            capturing = false;
            Serial.println("Capture complete");
            run_inference();
        }
    }
}

/**
 * @brief      Run local inference then decide whether to offload
 */
void run_inference() {
    if (sample_count * 3 < EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE) {
        Serial.println("ERROR: Not enough data for inference");
        return;
    }

    ei_impulse_result_t result = { 0 };

    signal_t features_signal;
    features_signal.total_length = EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE;
    features_signal.get_data = &raw_feature_get_data;

    // Time local inference
    unsigned long inference_start = millis();
    EI_IMPULSE_ERROR res = run_classifier(&features_signal, &result, false);
    unsigned long inference_latency = millis() - inference_start;

    if (res != EI_IMPULSE_OK) {
        Serial.print("ERR: Failed to run classifier (");
        Serial.print(res);
        Serial.println(")");
        return;
    }

    // Find prediction with highest confidence
    float max_value = 0;
    int max_index = -1;
    for (uint16_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
        if (result.classification[i].value > max_value) {
            max_value = result.classification[i].value;
            max_index = i;
        }
    }

    float confidence = max_value * 100.0;
    const char* gesture = ei_classifier_inferencing_categories[max_index];

    // ---- Offloading decision ----
    if (confidence >= CONFIDENCE_THRESHOLD) {
        // High confidence: use local result
        Serial.print("LOCAL_INFERENCE: ");
        Serial.print(gesture);
        Serial.print(" (");
        Serial.print(confidence, 1);
        Serial.print("%) latency=");
        Serial.print(inference_latency);
        Serial.println("ms");

        // ==============================================================
        // TODO 2: Add LED actuation for local inference path
        //         e.g., green LED on for "V", blue LED on for "O", etc.
        // ==============================================================

    } else {
        // Low confidence: offload to cloud
        Serial.print("OFFLOAD_TO_CLOUD: ");
        Serial.print(gesture);
        Serial.print(" (");
        Serial.print(confidence, 1);
        Serial.println("%) -> sending to server");

        sendRawDataToServer();
    }
}

/**
 * @brief      Send raw feature data to the Flask server for cloud inference
 */
void sendRawDataToServer() {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi not connected, attempting reconnect...");
        connectWiFi();
    }

    HTTPClient http;
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");
    http.setTimeout(5000);

    // Build JSON payload with feature array
    // Using ArduinoJson v7 (JsonDocument replaces deprecated DynamicJsonDocument)
    JsonDocument doc;
    JsonArray dataArray = doc["data"].to<JsonArray>();
    for (int i = 0; i < FEATURE_SIZE; i++) {
        dataArray.add(features[i]);
    }

    String jsonPayload;
    serializeJson(doc, jsonPayload);

    // Time the HTTP round-trip
    unsigned long cloud_start = millis();
    int httpResponseCode = http.POST(jsonPayload);
    unsigned long cloud_latency = millis() - cloud_start;

    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {
        String response = http.getString();

        // Parse JSON response
        JsonDocument respDoc;
        DeserializationError error = deserializeJson(respDoc, response);
        if (!error) {
            const char* gesture = respDoc["gesture"];
            float confidence = respDoc["confidence"];

            Serial.print("CLOUD_INFERENCE: ");
            Serial.print(gesture);
            Serial.print(" (");
            Serial.print(confidence, 1);
            Serial.print("%) latency=");
            Serial.print(cloud_latency);
            Serial.println("ms");

            // ==============================================================
            // TODO 3: Add LED actuation for cloud inference path
            //         e.g., same LED logic as TODO 2 but based on cloud result
            // ==============================================================

        } else {
            Serial.print("Failed to parse server response: ");
            Serial.println(error.c_str());
        }
    } else {
        Serial.printf("Error sending POST: %s\n",
                       http.errorToString(httpResponseCode).c_str());
    }

    http.end();
}

/**
 * @brief      Arduino main loop
 */
void loop() {
    // Check for serial commands
    if (Serial.available() > 0) {
        char cmd = Serial.read();
        if (cmd == 'o') {
            Serial.println("Starting gesture capture...");
            sample_count = 0;
            capturing = true;
            capture_start_time = millis();
            last_sample_time = millis();
        }
    }

    // Capture data if in capturing mode
    if (capturing) {
        capture_accelerometer_data();
    }
}
