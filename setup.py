import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gsodpy",
    version="0.0.1",
    author="Will Norris",
    author_email="willnorris303@gmail.com",
    description="A basic package for downloading and processing GSOD data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wino6687/gsodpy",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)