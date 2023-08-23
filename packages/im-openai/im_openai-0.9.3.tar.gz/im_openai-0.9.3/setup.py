#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

test_requirements = ["pytest>=3", "langchain"]

setup(
    author="Alec Flett",
    author_email="alec@thegp.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Wrapper library for openai to send events to the Imaginary Programming monitor",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="im_openai",
    name="im_openai",
    packages=find_packages(include=["im_openai", "im_openai.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/alecf/im_openai",
    version="0.9.3",
    zip_safe=False,
)
