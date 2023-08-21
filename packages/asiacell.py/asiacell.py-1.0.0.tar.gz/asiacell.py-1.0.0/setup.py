from setuptools import setup, find_packages
from asiacell import __version__, __author__, __lib_name__

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name=__lib_name__,
    version=__version__,
    url="https://github.com/ahmadelbd/Asiacell",
    download_url="https://github.com/ahmadelbd/Asiacell/archive/refs/heads/main.zip",
    description="Unofficial Python wrapper for Asiacell API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email="mustafadev.py@gmail.com",
    license="MIT",
    keywords=[
        "asiacell",
        "asiacell.py"
        "asia",
        "asiacell-api",
        "ahmadelbd",
        "lsfr",
        "asiacell-wrapper",
        "asiacell-bot"
    ],
    include_package_data=True,
    install_requires=[
        "requests",
        "ujson"
    ],
    setup_requires=["wheel"],
    packages=find_packages(),
)
