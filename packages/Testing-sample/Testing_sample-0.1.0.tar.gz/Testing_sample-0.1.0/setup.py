from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Testing_sample",
    version="0.1.0",
    author="venkateshwaran",
    author_email="venkateshwaranns@gmail.com",
    description="A short description of your package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/venkateshwaranns/testing.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas","unittest"
    ],
)
