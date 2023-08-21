from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name="cglearnlatest",
    version="0.6",
    author="shantanu",
    author_email="ssppdd18@gmail.com",
    description="Description of your package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=find_packages(where="cglearnlatest"),
    package_dir={"": "cglearnlatest"},
    package_data={
        "" : ["*.csv", "*.dll", "*.so"],
        "cglearnlatest" : ["*.csv", "*.dll", "*.so"],
    },
    include_package_data=True,
    install_requires=[
        "numpy",
        "networkx",
        "matplotlib",
        "pandas",
        "igraph",
        "scipy",
    ],
    extras_require={
        "extras": [
            # List your optional dependencies here
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
