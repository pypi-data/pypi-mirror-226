
# ca-visionlearn

The `ca-visionlearn` package offers a suite of tools tailored for image analysis, including color extraction, metric computation, skin tone identification, and more.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Image Color Analyzer](#image-color-analyzer)
3. [ImageMetrics](#imagemetrics)
4. [ProductColor](#productcolor)
5. [skin_tone Extraction](#skin_tone-extraction)
6. [Dependencies](#dependencies)

---

### Getting Started

Welcome to the `ca-visionlearn` starter guide. This notebook will walk you through the basic usage of the `ca-visionlearn` package using a sample image.

---

### Installation
```python
!pip install ca-visionlearn==3.1
```

---

### Importing Modules
```python
from ca_visionlearn.color_utils import ImageColorAnalyzer
from ca_visionlearn.metrics import ImageMetrics
from ca_visionlearn.product_color_processor import ProductColor
from ca_visionlearn.skin_tone_extraction import skin_tone
from PIL import Image
import matplotlib.pyplot as plt
import cv2
```

---

### Importing Dataset
```python
# Load the image
image_path = '/content/blue_dress.JPG'
image_array = cv2.imread(image_path) #OpenCV loads images in BGR by default and please do not change it
```

---

### Image Color Analyzer

This module provides the `ImageColorAnalyzer` class which facilitates the analysis of image colors. Specifically, it can compute the average, dominant, and background colors from an image.

**Features**:
- **Average Color Calculation**: Computes the average color of the image.
- **Dominant Color Calculation**: Utilizes k-means clustering to pinpoint the dominant color of the image.
- **Background Color Detection**: Determines the background color either by selecting the most common color (if it represents more than 50% of the image) or by averaging the 10 most common colors.

**Usage**:
Ensure the module is either in your Python path or in the same directory as your script. Then, you can utilize the following code:

```python
#Simple Starter
print("\n" + "*" * 50 + "\nstarter\n" + "*" * 50)

# Initialize the color analyzer and display results
analyzer = ImageColorAnalyzer(image_array)
analyzer.display_results()

#Extended
print("\n" + "*" * 50 + "\nExtended\n" + "*" * 50)

"""
# Display individual color analyses
analyzer.display_results(['average_color'])

# Display multiple types of color analyses
analyzer.display_results(['average_color', 'dominant_color', 'background_color'])

# Print color values without visualizing them:

# Average Color
print(f"Average Color: {analyzer.get_average_color()}")

# Dominant Color
print(f"Dominant Color: {analyzer.get_dominant_color()}")

# Background Color
print(f"Background Color: {analyzer.get_background_color()}")

"""

```

---

### ImageMetrics

The `ImageMetrics` class offers a suite of functions to compute various metrics on images, aiding in image analysis and quality assessment.

**Features**:
- **Contrast**: Measures the variance of pixel values in the image.
- **Brightness**: Computes the median pixel value of the image.
- **Sharpness**: Determines the variance of the Laplacian of the image.
- **Entropy**: Calculates the Shannon entropy, signifying the amount of information/content in the image.
- **Color Difference**: Finds the maximum Euclidean distance between color channels.
- **Color Saturation**: Measures the average saturation in the image.
- **Edge Density**: Represents the proportion of edges in the image.
- **Noise Estimate**: Calculates the difference between the original and a Gaussian-blurred version of the image.

**Usage**:
First, import the `ImageMetrics` class. To initialize the class, you should pass an image array to it. The `calculate_metrics` method can compute all available metrics by default. However, you can specify the metrics you desire by passing them as a list:

```python
#Simple Starter
print("\n" + "*" * 50 + "\nstarter\n" + "*" * 50)

# Initialize the metrics analyzer and get all metrics
analyzer = ImageMetrics(image_array)
all_metrics = analyzer.calculate_metrics()

# Print all metrics
for metric_name, value in all_metrics.items():
    print(f"{metric_name}: {value}")

#Extended
print("\n" + "*" * 50 + "\nExtended\n" + "*" * 50)


# Get individual metrics
contrast = analyzer.contrast()
brightness = analyzer.brightness()
sharpness = analyzer.sharpness()
entropy = analyzer.entropy()
color_difference = analyzer.color_difference()
color_saturation = analyzer.color_saturation()
edge_density = analyzer.edge_density()
noise_estimate = analyzer.noise_estimate()

# Print individual metrics
print("\nIndividual Metrics:")
print(f"Contrast: {contrast}")
print(f"Brightness: {brightness}")
print(f"Sharpness: {sharpness}")
print(f"Entropy: {entropy}")
print(f"Color Difference: {color_difference}")
print(f"Color Saturation: {color_saturation}")
print(f"Edge Density: {edge_density}")
print(f"Noise Estimate: {noise_estimate}")

```

---

### ProductColor

The `ProductColor` class is intricately designed to process images, mask human colors, distinguish between foreground and background, and extract dominant colors from the image.

**Methods**:
- `mask_human_colors()`: Masks human skin and hair colors.
- `separate_foreground_background()`: Differentiates between foreground and background based on edges and contours.
- `extract_dominant_colors(mask, n_clusters=3)`: Draws out dominant colors from the masked image.
- `extract_background_colors(n_clusters=3)`: Extracts dominant colors from the image's background.
- `check_center_mask(mask, region_size=50)`: Assesses if the mask's center is potentially misclassified as background.
- `process()`: Executes all processing steps on the image, preparing it for color extraction.
- `get_product_color()`: Yields the dominant product color along with a misclassification flag.
- `display_results()`: Provides a visualization of the various processing stages and the extracted colors.

**Usage**:
To utilize the `ProductColor` class, start by importing it. Subsequently, you can create an instance by offering your image array in BGR format. After initializing, it's possible to retrieve the dominant product color and a flag indicating potential misclassification at the center of the image:

```python
# Create an instance of the ProductColor class
analyzer = ProductColor(image_array)

# Process the image to extract colors
analyzer.get_product_color()

# Display the product color and misclassification flag
print("Product Color:", analyzer.product_color)
print("Misclassification Flag:", analyzer.misclassification_flag)

analyzer.display_results()

```

---

### skin_tone Extraction

This module is equipped with functionalities to extract and analyze the dominant skin tone from an image.

**Methods**:
- `extract_skin`: Carves out skin regions from an image.
- `remove_black`: Eradicates black regions from a clustered image.
- `get_color_information`: Fetches color distribution data from a clustered image.
- `extract_dominant_color`: Draws out the dominant color from an image.
- `plot_color_bar`: Produces a color bar grounded in color distribution.
- `pretty_print_data`: Displays color data in a user-friendly manner.
- `display_results`: Shows the original, thresholded, and color bar images.
- `get_rgb`: Gives the RGB value of the dominant skin tone.

**Usage**:
Begin by importing the `skin_tone` class. Once done, you can create an instance by providing the image path. After that, the dominant RGB value of the skin tone can be obtained:

```python
# Create an instance of the skin_detector class
skin_detector = skin_tone(image_array)

# Visualize the results including original image, thresholded image, and color bar
skin_detector.display_results()

# Get the RGB value of the skin tone
dominant_skin = skin_detector.get_dominant_skin_tone()
print(dominant_skin)


```

---

### Dependencies

Ensure the following Python libraries are installed in your environment:
- numpy
- cv2 (OpenCV)
- PIL (Pillow)
- skimage

---