import os
import setuptools

# get key package details from __version__.py file
about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'TauLidarCamera', '__version__.py')) as f:
    exec(f.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about['__url__'],
    packages=setuptools.find_packages(),
    install_requires=[
        'TauLidarCommon',
        'pyserial'
    ],
    license=about['__license__'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.1',
)
