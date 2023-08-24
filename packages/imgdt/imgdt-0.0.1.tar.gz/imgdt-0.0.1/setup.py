from setuptools import setup

VERSION  =  "0.0.1"

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "imgdt",
    version = VERSION,
    author = "MikiTwenty",
    author_email = "terminetor.xx@gmail.com",
    description = "Small package to prepare images for a dataset.",
    packages = ["imgdt"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/MikiTwenty/Python/tree/main/Libraries/video-streaming",
    keywords = ["python", "dataset", "transformer", "images"],
    license = "MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    install_requires = ["Pillow"]
)