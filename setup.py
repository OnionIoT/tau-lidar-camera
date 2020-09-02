import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tau-lidar-camera-OnionIoT", # Replace with your own username
    version="0.0.1",
    author="Onion Corporation",
    author_email="hello@onion.io",
    description="Tau Lidar Camera communication and configuration package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OnionIoT/tau-lidar-camera",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
