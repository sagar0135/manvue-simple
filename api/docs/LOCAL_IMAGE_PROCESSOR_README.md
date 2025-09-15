# Local Image Processor Service

The `LocalImageProcessor` is a comprehensive service for handling local image processing, copying, and embedding generation for dataset integration with the ManVue website.

## Features

- **Image Copying**: Copy dataset images to the website's images folder
- **Direct Processing**: Process images directly from the filesystem (bypassing HTTP server)
- **HTTP Processing**: Process images via local HTTP server
- **Image Validation**: Validate image files and get image information
- **Progress Tracking**: Built-in progress bars and logging
- **Error Handling**: Robust error handling with retry mechanisms

## Installation

The required dependencies are already included in `api/requirements.txt`:

```bash
pip install -r requirements.txt
```

Additional dependencies:
- `pandas` - For DataFrame handling
- `tqdm` - For progress bars
- `Pillow` - For image processing
- `requests` - For HTTP requests

## Quick Start

### Basic Usage

```python
from services.local_image_processor import LocalImageProcessor
import pandas as pd

# Initialize processor
processor = LocalImageProcessor(
    local_base_url="http://127.0.0.1:5500",
    images_folder="frontend/images"
)

# Load your dataset
df = pd.read_csv("your_dataset.csv")

# Process images directly from source
docs = processor.process_local_images_directly(
    df, 
    source_image_dir="/path/to/your/images",
    num_samples=10
)
```

### Complete Setup

```python
# Complete setup with both copying and processing
docs = processor.setup_local_website_images(
    df,
    source_image_dir="/path/to/your/images", 
    num_samples=10
)
```

## API Reference

### LocalImageProcessor

#### Constructor

```python
LocalImageProcessor(local_base_url="http://127.0.0.1:5500", images_folder="frontend/images")
```

**Parameters:**
- `local_base_url` (str): Base URL for the local development server
- `images_folder` (str): Folder name for images in the frontend

#### Methods

##### `copy_dataset_images_to_website(df, source_image_dir, num_samples=10)`

Copy images from your dataset to the website's images folder.

**Parameters:**
- `df` (DataFrame): DataFrame containing product information
- `source_image_dir` (str): Path to source images directory
- `num_samples` (int): Number of samples to process

**Returns:**
- `List[Dict]`: List of copied product dictionaries

##### `process_local_images_directly(df, source_image_dir, num_samples=5)`

Process images directly from local filesystem (bypass HTTP server).

**Parameters:**
- `df` (DataFrame): DataFrame containing product information
- `source_image_dir` (str): Path to source images directory
- `num_samples` (int): Number of samples to process

**Returns:**
- `List[Dict]`: List of processed document dictionaries

##### `get_image_embedding_local(image_url, max_retries=3)`

Get image embedding from local server with error handling.

**Parameters:**
- `image_url` (str): URL of the image to process
- `max_retries` (int): Maximum number of retry attempts

**Returns:**
- `PIL.Image` or `None`: PIL Image object or None if failed

##### `setup_local_website_images(df, source_image_dir, num_samples=5)`

Complete setup for local website with dataset images.

**Parameters:**
- `df` (DataFrame): DataFrame containing product information
- `source_image_dir` (str): Path to source images directory
- `num_samples` (int): Number of samples to process

**Returns:**
- `List[Dict]`: List of processed document dictionaries

##### `validate_image(image_path)`

Validate that an image file is valid and can be opened.

**Parameters:**
- `image_path` (str): Path to the image file

**Returns:**
- `bool`: True if image is valid, False otherwise

##### `get_image_info(image_path)`

Get basic information about an image file.

**Parameters:**
- `image_path` (str): Path to the image file

**Returns:**
- `Dict` or `None`: Dictionary with image information or None if invalid

## Usage Examples

### Example 1: Basic Image Processing

```python
import pandas as pd
from services.local_image_processor import LocalImageProcessor

# Load your dataset
df = pd.read_csv("products.csv")

# Initialize processor
processor = LocalImageProcessor()

# Process images directly
docs = processor.process_local_images_directly(
    df, 
    source_image_dir="/path/to/images",
    num_samples=5
)

print(f"Processed {len(docs)} images")
```

### Example 2: Copy Images to Website

```python
# Copy images to website folder
products = processor.copy_dataset_images_to_website(
    df,
    source_image_dir="/path/to/images",
    num_samples=10
)

# Images are now available at URLs like:
# http://127.0.0.1:5500/frontend/images/product1.jpg
```

### Example 3: Complete Setup

```python
# Complete setup with both copying and processing
docs = processor.setup_local_website_images(
    df,
    source_image_dir="/path/to/images",
    num_samples=10
)

# Save results
import pandas as pd
results_df = pd.DataFrame(docs)
results_df.to_csv("processed_images.csv", index=False)
```

### Example 4: Image Validation

```python
# Validate individual images
is_valid = processor.validate_image("path/to/image.jpg")
if is_valid:
    info = processor.get_image_info("path/to/image.jpg")
    print(f"Image size: {info['size']}")
    print(f"Image mode: {info['mode']}")
```

## Data Format

### Input DataFrame

Your DataFrame should contain the following columns:

- `image` (str): Image filename
- `display name` (str): Product display name
- `description` (str): Product description
- `category` (str): Product category

### Output Documents

Processed documents contain:

```python
{
    "title": "Product Name",
    "description": "Product Description", 
    "category": "Product Category",
    "image_filename": "image.jpg",
    "local_path": "/full/path/to/image.jpg",
    "image_url": "http://127.0.0.1:5500/frontend/images/image.jpg",
    "embedding": <PIL.Image object>,  # Replace with actual embedding
    "status": "success"
}
```

## Local Server Setup

To serve images via HTTP, you need a local server running:

### Option 1: Python HTTP Server

```bash
# From the project root directory
python -m http.server 5500
```

### Option 2: Live Server (VS Code)

1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Option 3: Node.js HTTP Server

```bash
# Install http-server globally
npm install -g http-server

# Start server
http-server -p 5500
```

## Error Handling

The service includes comprehensive error handling:

- **Connection Errors**: Automatic retry with exponential backoff
- **Image Validation**: Checks for valid image files
- **File System Errors**: Handles missing files and permissions
- **Network Errors**: Handles HTTP request failures

## Logging

The service uses Python's logging module with INFO level by default. To change the logging level:

```python
import logging
logging.getLogger('services.local_image_processor').setLevel(logging.DEBUG)
```

## Testing

Run the test suite to verify everything works:

```bash
cd api
python scripts/test_local_image_processor.py
```

## Integration with ManVue

The LocalImageProcessor integrates seamlessly with the ManVue project:

1. **Images Folder**: Images are copied to `frontend/images/`
2. **URL Generation**: Generates proper URLs for the frontend
3. **Database Integration**: Can be extended to store results in MongoDB
4. **ML Integration**: Ready for embedding generation and ML processing

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install required dependencies with `pip install -r requirements.txt`
2. **Connection Errors**: Make sure your local server is running on port 5500
3. **Permission Errors**: Check file permissions for the images directory
4. **Image Loading Errors**: Verify image files are valid and not corrupted

### Debug Mode

Enable debug logging for more detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

When extending the LocalImageProcessor:

1. Follow the existing code style
2. Add proper type hints
3. Include docstrings for new methods
4. Add tests for new functionality
5. Update this README if needed

## License

This service is part of the ManVue project and follows the same license terms.
