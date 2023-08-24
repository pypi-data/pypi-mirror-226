
# ca-visionlearn

The `ca-visionlearn` package offers a suite of tools tailored for image analysis, including color extraction, metric computation, skin tone identification, and more.

## Table of Contents
1. [Image Color Analyzer](#image-color-analyzer)
2. [ImageMetrics](#imagemetrics)
3. [ProductColor](#productcolor)
4. [skin_tone Extraction](#skin_tone-extraction)
5. [Dependencies](#dependencies)

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
from ca_visionlearn.color_utils import ImageColorAnalyzer

# Assuming image_array is your image data in the form of a numpy array:
analyzer = ImageColorAnalyzer(image_array)

# To obtain the average color:
avg_color = analyzer.get_average_color()

# To retrieve the dominant color:
dominant_color = analyzer.get_dominant_color()

# To get the background color:
background_color = analyzer.get_background_color()

# To display all results:
analyzer.display_results()
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
from ca_visionlearn.features_metric.metrics import ImageMetrics
from PIL import Image
import numpy as np

image = Image.open('path_to_your_image.jpg')
image_array = np.array(image)
metrics_calculator = ImageMetrics(image_array)

# For all metrics:
metrics = metrics_calculator.calculate_metrics()
print(metrics)

# For specific metrics:
metrics = metrics_calculator.calculate_metrics(metrics_list=['Contrast', 'Brightness'])
print(metrics)
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
from ca_visionlearn.product_color_processor import ProductColor

processor = ProductColor(img_array)

# To get dominant product color and misclassification flag:
color, misclassification_flag = processor.get_product_color()

# To visualize the results:
processor.display_results()
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
from ca_visionlearn.skin_tone_extraction import skin_tone

analyzer = skin_tone("path_to_image.jpg")

# To get the dominant RGB value of the skin tone:
dominant_rgb = analyzer.get_rgb()
print("Dominant Skin Tone RGB:", dominant_rgb)

# To visualize the results:
analyzer.display_results()
```

---

### Dependencies

Ensure the following Python libraries are installed in your environment:
- numpy
- cv2 (OpenCV)
- PIL (Pillow)
- skimage

---


### Dependencies

Ensure the following Python libraries are installed in your environment:
- cv2 (OpenCV)
- numpy
- PIL (from PIL import Image)
- collections (specifically the Counter)
- skimage.measure (specifically shannon_entropy)
- sklearn.cluster (specifically KMeans)
- matplotlib.pyplot
- imutils
- pprint