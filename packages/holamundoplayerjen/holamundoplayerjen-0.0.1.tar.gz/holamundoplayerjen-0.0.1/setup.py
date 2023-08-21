import setuptools
from pathlib import Path

long_desk = Path("README.md").read_text()
setuptools.setup(
    name="holamundoplayerjen",
    version="0.0.1",
    long_description=long_desk,
    packages=setuptools.find_packages(
        exclude=["mocks", "tests"]
    )
)
