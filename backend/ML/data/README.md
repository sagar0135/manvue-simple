# MANVUE ML Data

This directory contains datasets and data processing utilities for MANVUE's machine learning models.

## Directory Structure

```
data/
├── raw/                    # Raw, unprocessed data
│   ├── fashion_mnist/      # Fashion-MNIST dataset
│   ├── manvue_products/    # MANVUE product images
│   └── user_uploads/       # User-uploaded images
├── processed/              # Preprocessed data ready for training
│   ├── train/              # Training dataset
│   ├── validation/         # Validation dataset
│   └── test/               # Test dataset
├── augmented/              # Data augmentation results
├── annotations/            # Labels and metadata
└── exports/                # Exported datasets
```

## Datasets

### 1. Fashion-MNIST
- **Source**: Zalando Research
- **Size**: 70,000 images (60k train + 10k test)
- **Format**: 28x28 grayscale images
- **Categories**: 10 fashion categories
- **Usage**: Base training dataset

### 2. MANVUE Product Images
- **Source**: MANVUE product catalog
- **Size**: Variable (growing dataset)
- **Format**: Various (resized to 28x28 for model)
- **Categories**: Men's fashion focused
- **Usage**: Fine-tuning and validation

### 3. User Upload Data
- **Source**: Visual search feature
- **Size**: Dynamic (user-generated)
- **Format**: Various formats (PNG, JPG, etc.)
- **Usage**: Continuous learning and model improvement

## Data Processing Pipeline

### 1. Data Ingestion
```python
# Download Fashion-MNIST
fashion_mnist = tf.keras.datasets.fashion_mnist
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
```

### 2. Preprocessing
- Normalize pixel values (0-255 → 0-1)
- Resize images to 28x28
- Convert to grayscale
- Apply data augmentation

### 3. MANVUE Adaptations
- Filter categories relevant to men's fashion
- Apply custom category mappings
- Weight classes based on business priorities

## Data Augmentation

Applied transformations:
- **Rotation**: ±15 degrees
- **Zoom**: 0.8-1.2x
- **Shift**: ±10% width/height
- **Flip**: Horizontal (where appropriate)
- **Brightness**: ±20%

## Category Mapping

### Fashion-MNIST → MANVUE
```python
CATEGORY_MAPPING = {
    0: 'T-shirt/top',     # → tops
    1: 'Trouser',         # → bottoms
    2: 'Pullover',        # → tops
    3: 'Dress',           # → excluded (men's store)
    4: 'Coat',            # → outerwear
    5: 'Sandal',          # → shoes
    6: 'Shirt',           # → tops
    7: 'Sneaker',         # → shoes
    8: 'Bag',             # → accessories
    9: 'Ankle boot'       # → shoes
}
```

## Data Quality

### Metrics Tracked
- **Image Quality**: Resolution, clarity, artifacts
- **Label Accuracy**: Manual verification samples
- **Distribution**: Class balance across categories
- **Diversity**: Style, color, brand variation

### Quality Checks
- Automated duplicate detection
- Manual quality review (10% sample)
- Label consistency validation
- Bias detection and mitigation

## Privacy and Ethics

### Data Handling
- **User Consent**: Required for uploaded images
- **Anonymization**: Remove personal identifiers
- **Retention**: Clear data lifecycle policies
- **Access Control**: Restricted data access

### Bias Mitigation
- **Demographic Balance**: Diverse representation
- **Cultural Sensitivity**: Global fashion awareness
- **Size Inclusivity**: Various body types and sizes
- **Style Diversity**: Multiple fashion preferences

## Usage Examples

### Loading Training Data
```python
import numpy as np
from tensorflow.keras.utils import to_categorical

# Load and preprocess
x_train = np.load('processed/train/images.npy')
y_train = np.load('processed/train/labels.npy')
y_train = to_categorical(y_train, 10)
```

### Data Augmentation
```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2]
)
```

## Continuous Learning

### Feedback Loop
1. **User Interactions**: Track search success rates
2. **Corrections**: Allow users to correct predictions
3. **New Data**: Incorporate corrected samples
4. **Retraining**: Periodic model updates

### Data Collection
- Visual search uploads
- User feedback on predictions
- Product catalog additions
- A/B testing results

## Data Security

### Storage
- **Encryption**: At rest and in transit
- **Backup**: Regular automated backups
- **Versioning**: Data lineage tracking
- **Compliance**: GDPR, CCPA adherence

### Access Control
- **Authentication**: Secure API access
- **Authorization**: Role-based permissions
- **Auditing**: Access logs and monitoring
- **Anonymization**: Remove PII before processing
