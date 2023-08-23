# color_utils.py

import cv2
import numpy as np
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt

class AverageColor:
    """Calculates the average color of an image."""
    
    def __init__(self, image_array):
        self.image = image_array
        
    def calculate(self):
        """Return the average color of the image."""
        average = self.image.mean(axis=0).mean(axis=0)
        return tuple(np.round(average, 1))

class DominantColor:
    """Calculates the dominant color using k-means clustering."""
    
    def __init__(self, image_array):
        self.image = image_array
        
    def calculate(self, n_colors=5):
        """Return the dominant color of the image."""
        pixels = np.float32(self.image.reshape(-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        dominant = palette[np.argmax(counts)]
        return tuple(np.round(dominant, 1))

class ColorRenderer:
    """Renders a given RGB color as an image."""
    
    def __init__(self, rgb):
        self.rgb = rgb

    def render(self):
        """Display the color."""
        w, h = 512, 512
        data = np.zeros((h, w, 3), dtype=np.uint8)
        r, g, b = self.rgb
        data[0:512, 0:512] = [r, g, b]
        img = Image.fromarray(data, 'RGB')
        img.show()

class BackgroundColor:
    """Calculates the background color of an image."""
    
    def __init__(self, image_array):
        self.image = image_array
        self.manual_count = {}
        self.w, self.h, self.channels = self.image.shape
        self.total_pixels = self.w * self.h

    def count(self):
        """Count occurrence of each color in the image."""
        for y in range(0, self.h):
            for x in range(0, self.w):
                RGB = (self.image[x, y, 2], self.image[x, y, 1], self.image[x, y, 0])
                if RGB in self.manual_count:
                    self.manual_count[RGB] += 1
                else:
                    self.manual_count[RGB] = 1

    def average_colour(self):
        """Compute the average of the top 10 most common colors."""
        red, green, blue = 0, 0, 0
        sample = 10
        for top in range(0, sample):
            red += self.number_counter[top][0][0]
            green += self.number_counter[top][0][1]
            blue += self.number_counter[top][0][2]
        return tuple(np.round([red/sample, green/sample, blue/sample], 1))

    def calculate(self):
        """Return the background color of the image."""
        self.count()
        self.number_counter = Counter(self.manual_count).most_common(20)
        percentage_of_first = float(self.number_counter[0][1]) / self.total_pixels
        if percentage_of_first > 0.5:
            return tuple(np.round(self.number_counter[0][0], 1))
        else:
            return self.average_colour()

class ImageColorAnalyzer:
    """Main class to analyze colors in an image."""

    def __init__(self, image_array):
        self.image = image_array

    def get_average_color(self):
        """Return the average color."""
        ac = AverageColor(self.image)
        return ac.calculate()
    
    def get_dominant_color(self):
        """Return the dominant color."""
        dc = DominantColor(self.image)
        return dc.calculate()
    
    def get_background_color(self):
        """Return the background color."""
        bc = BackgroundColor(self.image)
        return bc.calculate()
    
    def display_results(self):
        """Display the results."""
        avg_color = self.get_average_color()
        dominant_color = self.get_dominant_color()
        background_color = self.get_background_color()
        print(f"Average Color: {avg_color}")
        print(f"Dominant Color: {dominant_color}")
        print(f"Background Color: {background_color}")  

        # Create patches for average color
        avg_patch = np.ones(shape=self.image.shape, dtype=np.uint8) * np.uint8(avg_color)

        # Create patches for dominant color
        dom_patch = np.zeros(shape=self.image.shape, dtype=np.uint8)
        pixels = np.float32(self.image.reshape(-1, 3))
        n_colors = 5
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)

        indices = np.argsort(counts)[::-1]
        freqs = np.cumsum(np.hstack([[0], counts[indices] / float(counts.sum())]))
        rows = np.int_(self.image.shape[0] * freqs)

        for i in range(len(rows) - 1):
            dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])

        # Create patches for background color
        bg_patch = np.ones(shape=self.image.shape, dtype=np.uint8) * np.uint8(background_color)

        # Display the patches
        fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(18, 6))
        ax0.imshow(avg_patch)
        ax0.set_title(f'Average Color: {avg_color}')
        ax0.axis('off')
        ax1.imshow(dom_patch)
        ax1.set_title('Dominant Colors')
        ax1.axis('off')
        ax2.imshow(bg_patch)
        ax2.set_title(f'Background Color: {background_color}')
        ax2.axis('off')
        plt.tight_layout()
        plt.show()

# End of color_utils.py
