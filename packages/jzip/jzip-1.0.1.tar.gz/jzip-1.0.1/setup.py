import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="jzip",
    version="1.0.1",
    author="Jilani Shaik",
    author_email="iammrj.java@gmail.com",
    description="This package provides utilities to work with gzip compressed base64 content.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iammrj/JZip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
