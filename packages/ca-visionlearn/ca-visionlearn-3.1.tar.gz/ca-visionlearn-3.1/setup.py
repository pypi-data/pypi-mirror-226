from setuptools import setup, find_packages

setup(
    name='ca-visionlearn',
    version='3.1',  # Incrementing the version
    description='Computer Vision Learning Package',
    author='Shantanu Dave',
    author_email='daveshantanu1@gmail.com',
    url='https://github.com/sdave-connexion/ca-visionlearn',
    packages=find_packages(),  # Automatically discover and include all packages in the package directory
    install_requires=[
        'numpy',
        'opencv-python',
        'Pillow',
        'scikit-image',
        'scikit-learn',
        'imutils',
        'matplotlib'
    ]
)
