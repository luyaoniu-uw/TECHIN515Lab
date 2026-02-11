# TECHIN 515 -- Lab 2: Model Compression for Edge Deployment


## Objective

In this lab, you will explore model compression techniques to reduce the size of deep learning models for deployment on resource-constrained microcontrollers. You will apply three **post-training quantization** methods and one **pruning** technique to an EfficientNet-based model trained on the Cats vs. Dogs dataset, then evaluate whether any compressed model fits on an ESP32.

By the end of this lab, you will be able to:
1. **Explain** how quantization reduces model size by changing weight precision
2. **Apply** Float-16, Dynamic Range, and Integer quantization to a trained model
3. **Implement** magnitude-based pruning with sparsity scheduling
4. **Analyze** accuracy vs. size trade-offs and create comparison visualizations
5. **Evaluate** whether compressed models fit ESP32 memory constraints

---

## Prerequisites

- Python 3.9+
- Basic neural network concepts (layers, training, inference)
- Familiarity with Jupyter notebooks and matplotlib

---

## Setup Instructions

1. Create and activate the Conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate TECHIN515
   ```
2. Install additional packages (cells provided in the notebook):
   - `tensorflow_datasets`
   - `tensorflow_model_optimization`

> **macOS Apple Silicon users:** If TensorFlow fails to install, replace `tensorflow==2.7.0` with `tensorflow-macos==2.7.0` in `environment.yml`.

---

## Lab Structure

1. **Preparing the Dataset** -- download cats_vs_dogs via TFDS
2. **Loading the Model** -- EfficientNet B0 with custom dense head
3. **Compiling the Model** -- Adam optimizer, sparse categorical crossentropy
4. **Training the Model** -- fine-tune for 3 epochs (15 for best results)
5. **Evaluating the Model** -- baseline accuracy + TFLite conversion
6. **Float-16 Quantization** -- worked example, predict-then-run
7. **Dynamic Range Quantization** -- INT8 weights, float activations
8. **Integer Quantization** -- full INT8 with representative dataset calibration
9. **Model Pruning** -- magnitude-based, 50%→80% sparsity schedule
10. **Converting for ESP32** -- xxd conversion (reference only, model too large)

---

## Discussion Questions

Throughout the notebook, you will answer discussion questions covering:
- Theoretical vs. actual compression ratios
- Why different quantization methods affect accuracy differently
- The role of representative datasets in INT8 calibration
- Pruning sparsity experiments and trade-offs
- ESP32 feasibility and architecture selection strategies

---

## Deliverables

1. Completed notebook with all cells executed
2. All discussion question responses
3. 1-2 paragraph reflection comparing techniques and recommending a deployment strategy

---


## Troubleshooting

- **"Corrupt JPEG data" warnings** -- Normal for cats_vs_dogs dataset, safe to ignore
- **Out of memory** -- Reduce batch_size from 16 to 8
- **TensorFlow version errors** -- Ensure you activated the TECHIN515 conda environment
- **Apple Silicon install failure** -- Replace `tensorflow==2.7.0` with `tensorflow-macos==2.7.0` in environment.yml

---

## References

1. [LearnOpenCV -- TFLite Model Optimization](https://learnopencv.com/tensorflow-lite-model-optimization-for-on-device-machine-learning/)
2. [TensorFlow -- Pruning with Keras](https://www.tensorflow.org/model_optimization/guide/pruning/pruning_with_keras)
3. [TensorFlow -- Comprehensive Pruning Guide](https://colab.research.google.com/github/tensorflow/model-optimization/blob/master/tensorflow_model_optimization/g3doc/guide/pruning/comprehensive_guide.ipynb)
