import setuptools
from pathlib import Path

description = Path("README.md").read_text()

setuptools.setup(
    name="apiperu",
    version="0.0.1",
    long_description=description,
    packages=setuptools.find_packages(
        exclude=["mocks", "test"]
    )
)