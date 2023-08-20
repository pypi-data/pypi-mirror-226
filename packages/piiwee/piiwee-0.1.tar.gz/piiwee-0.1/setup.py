from setuptools import setup, find_packages


setup(
    name="piiwee",
    version="0.1",
    license="MIT",
    author="Jianshuo Wang",
    author_email="jianshuo@hotmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/jianshuo/piiwee",
    keywords="cache permission restful",
    install_requires=["peewee", "fastapi"],
)
