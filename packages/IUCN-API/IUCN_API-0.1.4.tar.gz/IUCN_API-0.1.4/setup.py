from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="IUCN_API",
    version="0.1.4",
    author="Awotoro Ebenezer",
    author_email="ebenco94@gmail.com",
    description="A Python client for the IUCN Red List API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebenco94/IUCN_API",
    packages=find_packages(),
    install_requires=["requests", "python-dotenv"],
    keywords=["IUCN", "Red list", "Extinction", "Animal", "plant", "IUCN API"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
