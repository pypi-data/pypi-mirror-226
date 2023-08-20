import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="infoplus",
    version="0.0.2",
    author="Yanzhou Mu, Xuance Zhou, Zhiyuan Peng",
    author_email="522022000027@smail.nju.edu.cn",
    description="torchinfoplus for pytorch and mindsporeinfoplus for mindspore",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pzy2000",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
