from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyperfstats",
    version="0.1.1",
    author="Anish Reddy",
    author_email="anishreddy3456@gmail.comm",
    description="A lightweight Python performance profiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Anish-Reddy-K/pyperfstats",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "psutil>=5.8.0",
        "matplotlib>=3.3.0",
        "pandas>=1.2.0",
        "click>=7.0",
    ],
    entry_points={
        "console_scripts": [
            "pyperfstats=pyperfstats.cli:cli",
        ],
    },
)