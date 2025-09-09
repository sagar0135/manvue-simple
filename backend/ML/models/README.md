# MANVUE ML Models

This directory contains the trained machine learning models for MANVUE's AI-powered features.

## Models

### 1. Fashion Classifier (`fashion_classifier.h5`)
- **Purpose**: Product categorization from images
- **Architecture**: Convolutional Neural Network (CNN)
- **Dataset**: Fashion-MNIST with MANVUE customizations
- **Accuracy**: ~90%+ on test set
- **Input**: 28x28 grayscale images
- **Output**: 10 fashion categories

### 2. Model Metadata (`model_metadata.json`)
- Contains model version, accuracy, and category mappings
- Used by the API for model information

## Model Categories

The model classifies items into these categories:

| Class | MANVUE Category | Relevance |
|-------|----------------|-----------|
| T-shirt/top | tops | high |
| Trouser | bottoms | high |
| Pullover | tops | high |
| Dress | excluded | none |
| Coat | outerwear | high |
| Sandal | shoes | medium |
| Shirt | tops | high |
| Sneaker | shoes | high |
| Bag | accessories | medium |
| Ankle boot | shoes | high |

## Usage

### Loading the Model
```python
import tensorflow as tf
model = tf.keras.models.load_model('fashion_classifier.h5')
```

### Making Predictions
```python
# Preprocess image to 28x28 grayscale
predictions = model.predict(preprocessed_image)
predicted_class = np.argmax(predictions[0])
```

## Integration

The model is integrated with MANVUE through:
1. **ML API Server** (`../api/ml_server.py`)
2. **Frontend Integration** (`../utils/ml_integration.js`)
3. **Visual Search** (Enhanced image recognition)

## Model Performance

### Overall Metrics
- **Test Accuracy**: 90%+
- **Inference Time**: ~0.8s
- **Model Size**: ~2MB
- **Framework**: TensorFlow/Keras

### MANVUE-Specific Performance
- **Men's Fashion Focus**: Optimized for male clothing items
- **Category Relevance**: High accuracy for relevant categories
- **Real-time Processing**: Suitable for web applications

## Retraining

To retrain the model with new data:

1. **Add training data** to `../data/` directory
2. **Run training notebook** in `../notebooks/`
3. **Deploy new model** via API endpoint `/retrain`

## Model Versioning

- **v1.0.0**: Initial Fashion-MNIST based model
- **v1.1.0**: MANVUE category optimizations (planned)
- **v2.0.0**: Custom dataset integration (planned)

## Notes

- Model files are not included in version control due to size
- Download from training pipeline or model registry
- For production, use model serving infrastructure
- Consider model quantization for mobile deployment
