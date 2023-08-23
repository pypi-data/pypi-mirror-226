
from setuptools import setup, find_packages

setup(
    name="ca-visionlearn",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "Pillow",
        "scikit-image",
        "scikit-learn",
        "imutils",
        "matplotlib",
        "pprint"
    ],
    author="Shantanu Dave",
    author_email="daveshantanu1@gmail.com",
    description="A package for various image analysis tasks.",
    license="MIT",
    keywords="image analysis color metrics",
    url="https://github.com/sdave-connexion/ca-visionlearn",
)

