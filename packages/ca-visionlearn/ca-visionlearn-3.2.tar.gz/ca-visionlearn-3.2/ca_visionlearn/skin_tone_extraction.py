
import numpy as np
import cv2
from sklearn.cluster import KMeans
from collections import Counter
import imutils
import pprint
from matplotlib import pyplot as plt

class skin_tone:
    """
    Extract and analyze the dominant skin tone from an image.

    Methods:
    - extract_skin: Extracts skin regions from an image.
    - remove_black: Removes black regions from a clustered image.
    - get_color_information: Retrieves color distribution info from a clustered image.
    - extract_dominant_color: Extracts the dominant color from an image.
    - plot_color_bar: Generates a color bar based on color distribution.
    - pretty_print_data: Prints color information in a readable manner.
    - display_results: Visualizes the original, thresholded, and color bar images.
    - get_rgb: Returns the RGB value of the dominant skin tone.

    Attributes:
    - image: Input image
    """

    def __init__(self, image_array):
        """Initialize the skin_tone object with an image array.
        
        Args:
        - image_array (ndarray): Image array in BGR format.
        """
        self.image = image_array.copy()
        self.image = imutils.resize(self.image, width=1000)

    def extract_skin(self, image):
        img = image.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_threshold = np.array([0, 48, 80], dtype=np.uint8)
        upper_threshold = np.array([20, 255, 255], dtype=np.uint8)

        skin_mask = cv2.inRange(img, lower_threshold, upper_threshold)
        skin_mask = cv2.GaussianBlur(skin_mask, (3, 3), 0)

        skin = cv2.bitwise_and(img, img, mask=skin_mask)
        return cv2.cvtColor(skin, cv2.COLOR_HSV2BGR)

    def remove_black(self, estimator_labels, estimator_cluster):
        occurance_counter = Counter(estimator_labels)
        def compare(x, y): return Counter(x) == Counter(y)

        has_black = False
        for x in occurance_counter.most_common(len(estimator_cluster)):
            color = [int(i) for i in estimator_cluster[x[0]].tolist()]
            if compare(color, [0, 0, 0]) == True:
                del occurance_counter[x[0]]
                has_black = True
                estimator_cluster = np.delete(estimator_cluster, x[0], 0)
                break

        return (occurance_counter, estimator_cluster, has_black)

    def get_color_information(self, estimator_labels, estimator_cluster, has_thresholding=False):
        if has_thresholding:
            occurance, cluster, black = self.remove_black(
                estimator_labels, estimator_cluster)
            occurance_counter = occurance
            estimator_cluster = cluster
        else:
            occurance_counter = Counter(estimator_labels)

        total_occurance = sum(occurance_counter.values())
        color_information = []

        for x in occurance_counter.most_common(len(estimator_cluster)):
            index = int(x[0])
            index = (index-1) if (has_thresholding and black and int(index) != 0) else index
            color = estimator_cluster[index].tolist()
            color_percentage = (x[1] / total_occurance)
            color_info = {"cluster_index": index, "color": color, "color_percentage": color_percentage}
            color_information.append(color_info)

        return color_information

    def extract_dominant_color(self, image, number_of_colors=5, has_thresholding=False):
        if has_thresholding:
            number_of_colors += 1

        img = image.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.reshape((img.shape[0] * img.shape[1]), 3)
        
        estimator = KMeans(n_clusters=number_of_colors, n_init='auto', random_state=0)
        estimator.fit(img)

        color_information = self.get_color_information(
            estimator.labels_, estimator.cluster_centers_, has_thresholding)

        return color_information

    def plot_color_bar(self, color_information):
        color_bar = np.zeros((100, 500, 3), dtype="uint8")
        top_x = 0

        for x in color_information:
            bottom_x = top_x + (x["color_percentage"] * color_bar.shape[1])
            color = tuple(map(int, x['color']))
            cv2.rectangle(color_bar, (int(top_x), 0), (int(bottom_x), color_bar.shape[0]), color, -1)
            top_x = bottom_x

        return color_bar

    def pretty_print_data(self, color_info):
        for x in color_info:
            print(pprint.pformat(x))
            print()

    def display_results(self):
        fig, ax = plt.subplots(2, 3, figsize=(15,8))

        # Original Image
        ax[0, 0].imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        ax[0, 0].set_title("Original Image")
        ax[0, 0].axis("off")

        # Thresholded Image
        skin = self.extract_skin(self.image)
        ax[0, 1].imshow(cv2.cvtColor(skin, cv2.COLOR_BGR2RGB))
        ax[0, 1].set_title("Thresholded Image")
        ax[0, 1].axis("off")

        # Dominant Skin Tone
        dominant_colors = self.extract_dominant_color(skin, has_thresholding=True)
        dominant_color = max(dominant_colors, key=lambda x: x["color_percentage"])
        formatted_rgb = tuple(round(val, 1) for val in dominant_color["color"])
        dominant_skin_patch = np.ones((300, 300, 3), dtype=np.uint8) * np.uint8(formatted_rgb)
        ax[0, 2].imshow(dominant_skin_patch)
        ax[0, 2].set_title(f"Dominant Skin Tone\n(RGB): {formatted_rgb}")
        ax[0, 2].axis("off")

        # Color Bar in the middle of the second row
        color_bar = self.plot_color_bar(dominant_colors)
        ax[1, 1].imshow(color_bar)
        ax[1, 1].set_title("Color Bar")
        ax[1, 1].axis("off")
        ax[1, 0].axis("off")  # Turn off the first plot in the second row
        ax[1, 2].axis("off")  # Turn off the third plot in the second row

        plt.tight_layout()
        plt.show()

        #self.pretty_print_data(dominant_colors) uncomment to get all the 5 cluster values

    def get_dominant_skin_tone(self):
        """Returns the dominant skin tone from the image."""
        skin = self.extract_skin(self.image)
        dominant_colors = self.extract_dominant_color(skin, has_thresholding=True)
        dominant_color = max(dominant_colors, key=lambda x: x["color_percentage"])
        formatted_rgb = tuple(round(val, 1) for val in dominant_color["color"])
        return f"Dominant Skin Tone (RGB): {formatted_rgb}"

