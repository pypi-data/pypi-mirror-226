from setuptools import setup


# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="piiwee",
    version="0.4",
    license="MIT",
    author="Jianshuo Wang",
    author_email="jianshuo@hotmail.com",
    url="https://github.com/jianshuo/piiwee",
    keywords="cache permission restful",
    install_requires=["peewee"],
    py_modules=["piiwee"],
    description="A simple cache and permission layer for peewee",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
