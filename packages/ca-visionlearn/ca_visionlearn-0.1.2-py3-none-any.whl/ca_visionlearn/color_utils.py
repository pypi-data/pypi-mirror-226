
import cv2
import numpy as np
from PIL import Image
from collections import Counter

class ImageColorAnalyzer:
    """
    This class analyzes the colors in an image. It provides methods to get average, dominant, 
    and background colors. The input to this class is an image array.
    """
    
    def __init__(self, image_array):
        """
        Initialize the class with the given image array.
        
        Parameters:
        - image_array (numpy array): The image data in the form of a numpy array.
        """
        self.image = image_array
        self.w, self.h, self.channels = self.image.shape
        self.total_pixels = self.w * self.h
        
    def get_average_color(self):
        """
        Returns the average color of the image.
        
        Returns:
        - tuple: A tuple representing the average RGB values (rounded to one decimal place).
        """
        average = self.image.mean(axis=0).mean(axis=0)
        return tuple(np.round(average, 1))
    
    def get_dominant_color(self, n_colors=5):
        """
        Uses k-means clustering to find the dominant color of the image.
        
        Parameters:
        - n_colors (int): Number of colors to use in the k-means clustering. Default is 5.
        
        Returns:
        - tuple: A tuple representing the dominant RGB values (rounded to one decimal place).
        """
        pixels = np.float32(self.image.reshape(-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        dominant = palette[np.argmax(counts)]
    
        return tuple(np.round(dominant, 1))
    
    def get_background_color(self):
        """
        Determines the background color by either taking the most common color (if it's 
        present in more than 50% of the image) or by averaging the 10 most common colors.
        
        Returns:
        - tuple: A tuple representing the background RGB values (rounded to one decimal place).
        """
        manual_count = {}
        for y in range(0, self.h):
            for x in range(0, self.w):
                RGB = (self.image[x, y, 2], self.image[x, y, 1], self.image[x, y, 0])
                if RGB in manual_count:
                    manual_count[RGB] += 1
                else:
                    manual_count[RGB] = 1
                    
        number_counter = Counter(manual_count).most_common(20)
        percentage_of_first = float(number_counter[0][1])/self.total_pixels
        
        if percentage_of_first > 0.5:
            return tuple(np.round(number_counter[0][0], 1))
        else:
            red = sum([item[0][0] for item in number_counter[:10]]) / 10
            green = sum([item[0][1] for item in number_counter[:10]]) / 10
            blue = sum([item[0][2] for item in number_counter[:10]]) / 10
            return tuple(np.round([red, green, blue], 1))

    def display_results(self):
        """
        Displays the average, dominant, and background colors of the image.
        """
        avg_color = self.get_average_color()
        dominant_color = self.get_dominant_color()
        background_color = self.get_background_color()
        
        print(f"Average Color: {avg_color}")
        print(f"Dominant Color: {dominant_color}")
        print(f"Background Color: {background_color}")

