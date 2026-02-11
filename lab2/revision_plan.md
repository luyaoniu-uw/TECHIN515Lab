# TECHIN 515 Lab 2: Model Compression for Edge Deployment

## Overview
(2-3 sentences: why compression matters for ESP32, what students will do)

## Learning Objectives
- Explain why model compression is necessary for edge deployment
- Apply three post-training quantization methods (float16, dynamic range, int8)
- Implement magnitude-based pruning with TensorFlow Model Optimization
- Measure and visualize size/accuracy tradeoffs
- Evaluate whether a model fits target hardware constraints

## Time Estimate
~2.5-3 hours

## Prerequisites
- Python 3.9+
- Basic neural network concepts (layers, training, inference)
- Familiarity with Jupyter notebooks and matplotlib

## Setup
(Cross-platform Conda instructions)

## Lab Structure
(Brief outline of 10 sections with what students do in each)

## Deliverables
1. Completed notebook with all cells executed
2. Three student-coded sections: size utility, results table, visualization
3. All discussion question responses
4. 1-2 paragraph reflection comparing techniques and recommending a deployment strategy

## Grading Rubric
| Component | Points |
|-----------|--------|
| Notebook execution & bug-free code | 20 |
| Student coding tasks (3 tasks) | 25 |
| Discussion question responses | 25 |
| Visualization (bar chart + scatter) | 15 |
| Final reflection | 15 |

## Troubleshooting
- "Corrupt JPEG data" warnings → Normal for cats_vs_dogs dataset, safe to ignore
- Cache dataset truncation warnings → Normal, related to steps_per_epoch
- Out of memory → Reduce batch_size from 16 to 8
- TensorFlow version errors → Ensure you activated the TECHIN515 conda environment