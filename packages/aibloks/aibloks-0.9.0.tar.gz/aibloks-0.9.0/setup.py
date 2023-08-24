#!/usr/bin/env python

import re
from setuptools import find_packages, setup

VERSION_FILE = "aibloks/__init__.py"
with open(VERSION_FILE) as version_file:
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",version_file.read(), re.MULTILINE)

if match:
    version = match.group(1)
else:
    raise RuntimeError(f"Unable to find version string in {VERSION_FILE}.")

with open("README.md") as readme_file:
    long_description = readme_file.read()

setup(
    name="aibloks",  # Required
    version=version,  # Required
    description="Client library for the Ai Bloks REST API",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional
    url="https://www.aibloks.com",
    project_urls={
        'Repository': 'https://github.com/aibloks/aibloks-python-sdk',
    },
    authors= ["Ai Bloks <support@aibloks.com>"], # Optional
    author_email="support@aibloks.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="ai,data,development",  # Optional
    package_dir={"": "."},  # Optional
    packages=["aibloks"],
    python_requires=">=3.10, <4",
    zip_safe=True,
)
