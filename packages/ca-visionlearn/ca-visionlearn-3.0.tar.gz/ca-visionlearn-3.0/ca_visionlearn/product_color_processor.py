import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


class ProductColor:
    def __init__(self, image_array):
        """
        Initialize the ProductColor class with an image array.
        
        Args:
        - image_array (np.array): A numpy array representation of the image.
        """
        self.image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        self.product_color = None
        self.background_color = None
        self.dominant_colors = None
        self.product_masked = None
        self.fg_mask = None
        self.misclassification_flag = False
    
    def mask_human_colors(self):
        """
        Mask the human skin and hair colors in the image.
        
        Returns:
        - np.array: Image with human colors masked.
        """
        hsv = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
        lower_hair = np.array([0, 0, 0], dtype=np.uint8)
        upper_hair = np.array([180, 255, 60], dtype=np.uint8)
        hair_mask = cv2.inRange(hsv, lower_hair, upper_hair)
        human_mask = cv2.bitwise_or(skin_mask, hair_mask)
        return cv2.bitwise_and(self.image, self.image, mask=~human_mask)
    
    def separate_foreground_background(self):
        """
        Separate the foreground and background of the image.
        
        Returns:
        - np.array: Mask of the foreground.
        """
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        dilated = cv2.dilate(edges, None, iterations=2)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros_like(gray, dtype=np.uint8)
        cv2.drawContours(mask, contours, -1, (255,), thickness=cv2.FILLED)
        return mask

    def extract_dominant_colors(self, image, mask, n_clusters=3):
        """
        Extract dominant colors from the image using KMeans clustering.
        
        Args:
        - mask (np.array): Mask to target specific region of the image.
        - n_clusters (int): Number of clusters for KMeans.
        
        Returns:
        - list: List of dominant colors in the image.
        """
        masked_image = cv2.bitwise_and(image, image, mask=mask.astype(np.uint8))
        pixels = masked_image.reshape(-1, 3)
        pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]
        if len(pixels) == 0:
            return [[0, 0, 0]]  # return black if no valid pixels
        kmeans = KMeans(n_clusters=n_clusters, n_init=10)
        kmeans.fit(pixels)
        cluster_sizes = np.bincount(kmeans.labels_)
        sorted_centers = [center for _, center in sorted(zip(cluster_sizes, kmeans.cluster_centers_), reverse=True)]
        return np.array(sorted_centers).astype(int).tolist()

    def check_center_mask(self, mask, region_size=50):
        """
        Check if the center of the mask is classified as background.
        
        Args:
        - mask (np.array): Mask to be checked.
        - region_size (int): Size of the center region to be checked.
        
        Returns:
        - bool: True if the center is misclassified as background, False otherwise.
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
    
    def get_product_color(self):
        """
        Main function to extract product and background colors from the image.
        This function will follow the steps in the order specified.
        """
        # Separate foreground and background
        self.fg_mask = self.separate_foreground_background()
        
        # Mask human colors
        masked_image = self.mask_human_colors()
        
        # Apply foreground mask
        self.product_masked = cv2.bitwise_and(masked_image, masked_image, mask=self.fg_mask.astype(np.uint8))
        
        # Extract dominant colors using the product mask
        self.dominant_colors = self.extract_dominant_colors(self.product_masked, self.fg_mask)
        
        # The most dominant color is considered the product color
        self.product_color = self.dominant_colors[0]
        
        # Extract dominant colors from the background
        background_colors = self.extract_dominant_colors(self.image, cv2.bitwise_not(self.fg_mask))
        
        # The most dominant color in the background is considered the background color
        self.background_color = background_colors[0]
        
        # Check if the center of the mask is classified as background
        self.misclassification_flag = self.check_center_mask(self.fg_mask)
        if self.misclassification_flag:
            print("Warning: The center of the image might be misclassified as background!")
    
    def display_results(self):
        """
        Display the results including original image, masked image, foreground mask, product color, dominant colors, and background color.
        """
        fig, ax = plt.subplots(1, 4, figsize=(30, 5))
        ax[0].imshow(self.image)
        ax[0].set_title("Original Image")
        ax[1].imshow(self.product_masked)
        ax[1].set_title("Image after Masking Human Colors")
        ax[2].imshow(self.fg_mask, cmap='gray')
        ax[2].set_title("Foreground Mask")
        ax[3].imshow([[self.product_color]])
        ax[3].set_title("Product Color")

        """
        Unhide to get dominent color and background color

        for i, color in enumerate(self.dominant_colors):
            if i + 4 < len(ax):
                ax[i + 4].imshow([[color]])
                ax[i + 4].set_title(f"Dominant Color {i+1}")
        ax[5].imshow([[self.background_color]])
        ax[5].set_title("Background Color")


        """
        plt.tight_layout()
        plt.show()

