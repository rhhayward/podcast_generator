import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="podcast_generator-rhhayward",
    version="0.0.1",
    author="Ryan Hayward",
    author_email="rhhayward@att.net",
    description="A package for downloading files, and making a podcast out of them",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rhhayward/podcast_generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'bs4',
        'requests',
    ],
    python_requires='>=3.6',
)
