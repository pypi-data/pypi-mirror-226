
import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

class ProductColor:
    def __init__(self, image_array):
        """
        Initialize the ProductColor object with an image array.
        
        Parameters:
        - image_array: A BGR image array.
        """
        self.image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        self.fg_mask = None
        self.product_masked = None
        self.dominant_colors = None
        self.background_colors = None

    def mask_human_colors(self):
        """
        Masks out human colors (skin and hair) from the image.
        """
        hsv = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        
        # Define HSV ranges for skin colors and mask them
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        # Define HSV ranges for hair colors and mask them
        lower_hair = np.array([0, 0, 0], dtype=np.uint8)
        upper_hair = np.array([180, 255, 60], dtype=np.uint8)
        hair_mask = cv2.inRange(hsv, lower_hair, upper_hair)
        
        # Combine the skin and hair masks
        human_mask = cv2.bitwise_or(skin_mask, hair_mask)
        
        # Apply the mask to the original image
        self.product_masked = cv2.bitwise_and(self.image, self.image, mask=~human_mask)

    def separate_foreground_background(self):
        """
        Separates the foreground (product) from the background.
        """
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        dilated = cv2.dilate(edges, None, iterations=2)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros_like(gray, dtype=np.uint8)
        cv2.drawContours(mask, contours, -1, (255,), thickness=cv2.FILLED)
        self.fg_mask = mask

    def extract_dominant_colors(self, mask, n_clusters=3):
        """
        Extracts dominant colors from the masked image.
        
        Parameters:
        - mask: The mask to apply on the image before extracting colors.
        - n_clusters: Number of dominant colors to extract.
        
        Returns:
        - List of dominant colors.
        """
        masked_image = cv2.bitwise_and(self.image, self.image, mask=mask)
        pixels = masked_image.reshape(-1, 3)
        pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]
        
        if len(pixels) == 0:
            return [[0, 0, 0]]  # return black if no valid pixels
        
        kmeans = KMeans(n_clusters=n_clusters, n_init=10)
        kmeans.fit(pixels)
        cluster_sizes = np.bincount(kmeans.labels_)
        sorted_centers = [center for _, center in sorted(zip(cluster_sizes, kmeans.cluster_centers_), reverse=True)]
        
        return np.array(sorted_centers).astype(int).tolist()

    def extract_background_colors(self, n_clusters=3):
        """
        Extracts dominant colors from the background of the image.
        
        Parameters:
        - n_clusters: Number of dominant colors to extract.
        """
        bg_mask = cv2.bitwise_not(self.fg_mask)
        self.background_colors = self.extract_dominant_colors(bg_mask, n_clusters=n_clusters)

    def check_center_mask(self, mask, region_size=50):
        """
        Checks if the center of the mask is classified as background.
        
        Parameters:
        - mask: The mask to check.
        - region_size: Size of the central region to check.
        
        Returns:
        - Boolean indicating if the central region is mostly background.
        """
        center_y, center_x = mask.shape[0] // 2, mask.shape[1] // 2
        start_y, end_y = center_y - region_size // 2, center_y + region_size // 2
        start_x, end_x = center_x - region_size // 2, center_x + region_size // 2
        center_region = mask[start_y:end_y, start_x:end_x]
        total_pixels = center_region.size
        background_pixels = (center_region == 0).sum()
        
        if background_pixels / total_pixels > 0.5:
            return True
        return False

    def process(self):
        """
        Process the image to separate foreground, background, mask human colors, 
        and extract dominant colors.
        """
        self.mask_human_colors()
        self.separate_foreground_background()
        self.dominant_colors = self.extract_dominant_colors(self.fg_mask)
        self.extract_background_colors()

    def get_product_color(self):
        """
        Processes the image and returns the dominant product color and misclassification flag.
        
        Returns:
        - Tuple containing:
            - Dominant product color as a list of RGB values rounded to one decimal place.
            - misclassification_flag: Boolean indicating if the central region is mostly background.
        """
        self.process()
        misclassification_flag = self.check_center_mask(self.fg_mask)
        dominant_color = [round(val, 1) for val in self.dominant_colors[0]]
        return dominant_color, misclassification_flag

    def display_results(self):
        """
        Display the original image, masked image, foreground mask, 
        dominant product color, and other dominant colors.
        """
        fig, ax = plt.subplots(1, 6, figsize=(30, 5))
        ax[0].imshow(self.image)
        ax[0].set_title("Original Image")
        ax[1].imshow(self.product_masked)
        ax[1].set_title("Image after Masking Human Colors")
        ax[2].imshow(self.fg_mask, cmap='gray')
        ax[2].set_title("Foreground Mask")
        ax[3].imshow([self.dominant_colors[0]])
        ax[3].set_title("Product Color")
        for i, color in enumerate(self.dominant_colors):
            if i + 4 < len(ax):
                ax[i + 4].imshow([color])
                ax[i + 4].set_title(f"Dominant Color {i+1}")
        ax[5].imshow([self.background_colors[0]])
        ax[5].set_title("Background Color")
        plt.tight_layout()
        plt.show()
