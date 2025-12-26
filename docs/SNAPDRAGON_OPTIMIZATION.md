# Snapdragon Optimization Guide

## Overview

This guide provides optimization strategies for running the Face Recognition Application on Qualcomm Snapdragon chipsets, leveraging their Neural Processing Unit (NPU), GPU, and DSP for accelerated AI inference.

## Current Implementation Status

**Current Setup:**
- Framework: TensorFlow/Keras via DeepFace
- Model: VGG-Face (default)
- Backend: OpenCV for face detection
- Format: Full precision (FP32)
- Execution: CPU-based inference

**Performance Characteristics:**
- Model size: ~500MB (VGG-Face)
- Inference time: ~500-1000ms per face (CPU)
- Memory usage: High

## Optimization Strategies for Snapdragon

### 1. **Model Quantization** (Highest Impact)

Convert models from FP32 to INT8 for significant performance gains.

**Benefits:**
- 4x smaller model size
- 2-4x faster inference
- Lower power consumption
- Better NPU utilization

**Implementation Options:**

#### Option A: TensorFlow Lite (TFLite) Conversion
```python
# Install TFLite converter
pip install tensorflow

# Convert DeepFace model to TFLite with quantization
import tensorflow as tf

# Post-training quantization
converter = tf.lite.TFLiteConverter.from_saved_model('model_path')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]  # or tf.int8
tflite_model = converter.convert()

# Save quantized model
with open('model_quantized.tflite', 'wb') as f:
    f.write(tflite_model)
```

#### Option B: ONNX Conversion + Quantization
```bash
# Install ONNX tools
pip install onnx onnxruntime onnxruntime-extensions

# Convert to ONNX (use deepface-onnx library)
pip install deepface-onnx

# Quantize ONNX model
python -m onnxruntime.quantization.preprocess --input model.onnx --output model_prep.onnx
python -m onnxruntime.quantization.quantize --input model_prep.onnx --output model_int8.onnx
```

### 2. **Qualcomm SNPE (Snapdragon Neural Processing Engine)**

**Best Performance on Snapdragon Devices**

SNPE enables direct execution on Snapdragon's NPU/DSP/GPU.

**Setup:**
1. Download Qualcomm SNPE SDK from Qualcomm Developer Network
2. Convert model to SNPE's DLC format
3. Deploy with hardware acceleration

```bash
# Convert ONNX to SNPE DLC
snpe-onnx-to-dlc --input_network model.onnx \
                 --output_path model.dlc

# Quantize for NPU
snpe-dlc-quantize --input_dlc model.dlc \
                  --output_dlc model_quantized.dlc \
                  --input_list calibration_data.txt
```

**Expected Performance:**
- 10-100x speedup over CPU
- Runs on NPU (45 TOPS on Snapdragon X Elite)
- Minimal battery impact

### 3. **Lightweight Model Alternatives**

Replace VGG-Face with mobile-optimized models.

**Recommended Models:**

| Model | Size | Speed | Accuracy | Snapdragon Optimized |
|-------|------|-------|----------|---------------------|
| **MobileFaceNet** | 4MB | Very Fast | 99.2% | ✅ Yes |
| **FaceNet-Mobile** | 23MB | Fast | 99.6% | ✅ Yes |
| **ArcFace-Mobile** | 15MB | Fast | 99.8% | ✅ Yes |
| VGG-Face (current) | 500MB | Slow | 98.9% | ❌ No |

**Implementation:**
```python
# In config.py, change to:
FACE_RECOGNITION_MODEL = "Facenet"  # Lighter than VGG-Face

# Or use custom MobileFaceNet (requires additional setup)
```

### 4. **NNAPI Integration (Android)**

If running on Android with Snapdragon, use NNAPI for automatic hardware acceleration.

```python
# Install TFLite with NNAPI support
pip install tensorflow-lite-nnapi

# Load model with NNAPI delegate
import tensorflow as tf

# Create NNAPI delegate
nnapi_delegate = tf.lite.experimental.load_delegate('libnnapi_delegate.so')

# Load interpreter with delegate
interpreter = tf.lite.Interpreter(
    model_path='model.tflite',
    experimental_delegates=[nnapi_delegate]
)
```

### 5. **Qualcomm AI Hub** (Easiest Path)

Use pre-optimized models from Qualcomm AI Hub.

**Steps:**
1. Visit: https://aihub.qualcomm.com/
2. Search for face recognition models
3. Download Snapdragon-optimized versions
4. Integrate into application

**Available Models:**
- MobileFaceNet (optimized for Hexagon NPU)
- Face detection models
- Pre-quantized and ready to deploy

### 6. **Multi-Threading & Batch Processing**

Optimize CPU usage while waiting for NPU support.

```python
# In face_recognition_module.py
import concurrent.futures

def process_faces_parallel(self, frames):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(self.process_single_face, frames))
    return results
```

### 7. **Reduce Resolution**

Lower camera resolution for faster processing.

```python
# In config.py
CAMERA_WIDTH = 320   # Reduced from 640
CAMERA_HEIGHT = 240  # Reduced from 480
```

## Recommended Implementation Path

### Phase 1: Quick Wins (Immediate - No Model Changes)
1. ✅ Switch to lighter model: `Facenet` instead of `VGG-Face`
2. ✅ Reduce camera resolution to 320x240
3. ✅ Use `ssd` or `mtcnn` detector instead of `opencv`
4. ✅ Implement frame skipping (process every 2-3 frames)

**Expected Improvement:** 2-3x faster

### Phase 2: Model Optimization (1-2 days)
1. Convert models to ONNX format
2. Apply INT8 quantization
3. Test accuracy vs performance tradeoff

**Expected Improvement:** 4-5x faster, 75% smaller

### Phase 3: Hardware Acceleration (1 week)
1. Install Qualcomm SNPE SDK
2. Convert to DLC format
3. Deploy with NPU acceleration

**Expected Improvement:** 10-50x faster on Snapdragon NPU

### Phase 4: Production Optimization (Ongoing)
1. Use Qualcomm AI Hub pre-optimized models
2. Implement NNAPI for Android deployment
3. Fine-tune quantization parameters

**Expected Improvement:** Near real-time performance (<50ms per face)

## Quick Configuration Changes

### Immediate Optimization (No Code Changes)

Edit `config.py`:

```python
# Optimized settings for Snapdragon
CAMERA_WIDTH = 320  # Reduced resolution
CAMERA_HEIGHT = 240

FACE_DETECTOR_BACKEND = "ssd"  # Faster than opencv
FACE_RECOGNITION_MODEL = "Facenet"  # Lighter than VGG-Face

FACE_MATCH_THRESHOLD = 0.7  # Slightly higher for faster matching
```

### Frame Processing Optimization

Edit `main.py`:

```python
# Change processing interval
process_interval = 60  # Process every 60 frames instead of 30
                       # Reduces CPU load by 50%
```

## Performance Benchmarks (Estimated)

| Configuration | Inference Time | Model Size | Accuracy | NPU Support |
|--------------|----------------|------------|----------|-------------|
| **Current (VGG-Face, CPU)** | 500-1000ms | 500MB | 98.9% | ❌ |
| **Facenet, CPU** | 200-400ms | 90MB | 99.6% | ❌ |
| **Facenet, TFLite INT8** | 100-200ms | 23MB | 99.4% | ⚠️ Partial |
| **MobileFaceNet, SNPE NPU** | 10-50ms | 4MB | 99.2% | ✅ Full |

## Tools & Resources

### Required Tools
- **TensorFlow Lite**: Model conversion and quantization
- **ONNX Runtime**: Cross-platform inference
- **Qualcomm SNPE SDK**: Snapdragon-specific optimization
- **Qualcomm AI Hub**: Pre-optimized models

### Installation
```bash
# TFLite tools
pip install tensorflow onnx onnxruntime

# SNPE SDK (requires Qualcomm Developer account)
# Download from: https://developer.qualcomm.com/software/qualcomm-neural-processing-sdk

# AI Hub CLI
pip install qai-hub
```

### Useful Links
- Qualcomm AI Hub: https://aihub.qualcomm.com/
- SNPE Documentation: https://developer.qualcomm.com/docs/snpe/
- TFLite Optimization: https://www.tensorflow.org/lite/performance/model_optimization

## Testing & Validation

### Accuracy Testing
```python
# Test quantized model accuracy
from deepface import DeepFace

# Compare original vs optimized
result_original = DeepFace.verify("img1.jpg", "img2.jpg", model_name="VGG-Face")
result_optimized = DeepFace.verify("img1.jpg", "img2.jpg", model_name="Facenet")

print(f"Accuracy difference: {abs(result_original['distance'] - result_optimized['distance'])}")
```

### Performance Profiling
```python
import time

start = time.time()
# Run inference
embedding = face_module.get_face_embedding(frame, face_region)
end = time.time()

print(f"Inference time: {(end - start) * 1000:.2f}ms")
```

## Conclusion

**Immediate Actions (Today):**
1. Change `FACE_RECOGNITION_MODEL = "Facenet"` in config.py
2. Reduce camera resolution to 320x240
3. Increase frame skip interval

**Short-term (This Week):**
1. Convert models to ONNX
2. Apply INT8 quantization
3. Test on Snapdragon device

**Long-term (Production):**
1. Implement SNPE for NPU acceleration
2. Use Qualcomm AI Hub models
3. Deploy with NNAPI on Android

**Expected Overall Improvement:** 10-100x faster with proper NPU utilization on Snapdragon chipsets.
