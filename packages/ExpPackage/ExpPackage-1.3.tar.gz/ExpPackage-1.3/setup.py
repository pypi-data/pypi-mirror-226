import setuptools
from pathlib import Path

setuptools.setup(
    name="ExpPackage",
    version=1.3,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=['tests', 'Data'])
)
