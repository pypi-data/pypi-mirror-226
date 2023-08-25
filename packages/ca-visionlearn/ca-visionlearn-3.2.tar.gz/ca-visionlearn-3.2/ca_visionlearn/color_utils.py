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
        return tuple(np.round(dominant, 1)), palette, counts  # Return additional information for visualization

class BackgroundColor:
    """Calculates the background color of an image."""
    
    def __init__(self, image_array):
        self.image = image_array

    def calculate(self):
        """Return the background color of the image."""
        # Using numpy to efficiently count occurrences of each color
        unique_colors, counts = np.unique(self.image.reshape(-1, 3), axis=0, return_counts=True)
        most_common_colors = unique_colors[np.argsort(-counts)[:20]]
        most_common_counts = counts[np.argsort(-counts)[:20]]
        
        percentage_of_first = float(most_common_counts[0]) / len(self.image)
        if percentage_of_first > 0.5:
            return tuple(np.round(most_common_colors[0], 1))
        else:
            return tuple(np.round(most_common_colors[:10].mean(axis=0), 1))

class ImageColorAnalyzer:
    """Main class to analyze colors in an image."""

    def __init__(self, image_array):
        self.image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

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

    def display_results(self, types=None):
        """Display and print the specified results."""
        
        if types is None:
            types = ['average_color', 'dominant_color', 'background_color']

        fig, axs = plt.subplots(1, len(types), figsize=(18, 6))

        # Ensure axs is always a list, even if there's only one subplot
        if len(types) == 1:
            axs = [axs]

        # For average color
        if 'average_color' in types:
            avg_color = self.get_average_color()
            print(f"Average Color: {avg_color}")
            avg_patch = np.ones(shape=self.image.shape, dtype=np.uint8) * np.uint8(avg_color)
            ax = axs[types.index('average_color')]
            ax.imshow(avg_patch)
            ax.set_title(f'Average Color')
            ax.axis('off')

        # For dominant color
        if 'dominant_color' in types:
            dominant_color, palette, counts = self.get_dominant_color()  # Fetch additional data
            print(f"Dominant Color: {dominant_color}")
            
            indices = np.argsort(counts)[::-1]
            freqs = np.cumsum(np.hstack([[0], counts[indices] / float(counts.sum())]))
            rows = np.int_(self.image.shape[0] * freqs)

            dom_patch = np.zeros_like(self.image, dtype=np.uint8)
            for i in range(len(rows) - 1):
                dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])
            ax = axs[types.index('dominant_color')]
            ax.imshow(dom_patch)
            ax.set_title('Dominant Colors')
            ax.axis('off')

        # For background color
        if 'background_color' in types:
            background_color = self.get_background_color()
            print(f"Background Color: {background_color}")
            bg_patch = np.ones(shape=self.image.shape, dtype=np.uint8) * np.uint8(background_color)
            ax = axs[types.index('background_color')]
            ax.imshow(bg_patch)
            ax.set_title(f'Background Color')
            ax.axis('off')

        plt.tight_layout()
        plt.show()

# Optimized code
