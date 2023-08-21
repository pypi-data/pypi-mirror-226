from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codepulse",
    version="0.1.0",
    author="codepulse",
    author_email="codepulsedevelopers@gmail.com",
    description="Measure execution time for each line of a function.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codepulse-developers/codepulse",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["pandas"],
)
