
import numpy as np
import cv2
from skimage.measure import shannon_entropy
from PIL import Image

class ImageMetrics:
    """ImageMetrics class provides functionalities to compute various image metrics.

    Attributes:
        image_array (numpy.ndarray): Input image in the form of a numpy array.
    
    Methods:
        calculate_metrics: Computes the selected image metrics.
    """
    
    def __init__(self, image_array):
        """
        Initializes the ImageMetrics with the provided image array.
        
        Args:
            image_array (numpy.ndarray): Input image in the form of a numpy array.
        """
        self.image_array = image_array

    def contrast(self):
        """Computes the contrast of the image."""
        return self.image_array.std()

    def brightness(self):
        """Computes the brightness of the image."""
        return np.median(self.image_array)

    def sharpness(self):
        """Computes the sharpness of the image."""
        return cv2.Laplacian(self.image_array, cv2.CV_64F).var()

    def entropy(self):
        """Computes the entropy of the image."""
        return shannon_entropy(self.image_array)

    def color_difference(self):
        """
        Computes the color difference of the image.
        
        This is calculated as the maximum Euclidean distance between the color channels.
        """
        colors = cv2.split(self.image_array)
        color_differences = [np.linalg.norm(colors[i] - colors[j]) for i in range(len(colors)) for j in range(i + 1, len(colors))]
        return max(color_differences)

    def color_saturation(self):
        """Computes the color saturation of the image."""
        hsv_image = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2HSV)
        saturation_channel = hsv_image[:, :, 1]
        return np.mean(saturation_channel) / 255.0

    def edge_density(self):
        """Computes the edge density of the image."""
        grayscale = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(grayscale, 100, 200)
        return np.mean(edges) / 255.0

    def noise_estimate(self):
        """Computes an estimate of the noise in the image."""
        blurred = cv2.GaussianBlur(self.image_array, (5, 5), 0)
        return np.mean(np.abs(self.image_array - blurred))

    def calculate_metrics(self, metrics_list=None):
        """
        Computes the selected image metrics.
        
        Args:
            metrics_list (list, optional): List of metric names to compute. If None, all metrics are computed.
            
        Returns:
            dict: Dictionary of computed image metrics.
        """
        all_metrics = {
            'Contrast': self.contrast,
            'Brightness': self.brightness,
            'Sharpness': self.sharpness,
            'Entropy': self.entropy,
            'Color Difference': self.color_difference,
            'Color Saturation': self.color_saturation,
            'Edge Density': self.edge_density,
            'Noise Estimate': self.noise_estimate
        }
        
        if metrics_list is None:
            metrics_list = all_metrics.keys()

        # Compute the selected metrics
        computed_metrics = {key: all_metrics[key]() for key in metrics_list}
        
        # Round all metrics to 3 decimal places
        return {key: np.round_(value, 3) for key, value in computed_metrics.items()}
