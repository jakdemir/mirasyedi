from setuptools import setup, find_packages

setup(
    name="inheritance-calculator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pydantic",
        "pytest"
    ]
) 