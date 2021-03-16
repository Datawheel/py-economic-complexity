from os import path

from setuptools import find_packages, setup

from complexity import __version__

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md")) as f:
    README = f.read()

setup(
    name="complexity",
    version=__version__,
    description="Functions to compute Economic Complexity measures.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Marcos Peréz",
    author_email="marcos@datawheel.us",
    url="",
    packages=find_packages(include=["complexity"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
