#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import setuptools


app_name = "kmd_hmdb_api_client"
current_dir = os.path.dirname(__file__)
version = "1.0.1"

if (os.path.exists(path := os.path.join(current_dir, "README.md"))):
  with open(path) as f:
    long_description = f.read()
else:
  long_description = "Not implemented yet"

requirements = [
  "attrs==23.1.0",
  "click==8.1.3",
  "httpx==0.24.1",
]

if __name__ == "__main__":
  setuptools.setup(
    name=app_name,
    python_requires=">=3.9.0",
    version=version,
    description="A API Client for KMD HMDB",
    long_description=long_description,
    author="Lainou",
    author_email="lain.pavot@inrae.fr",
    license="GNU GENERAL PUBLIC LICENSE v3",
    url="",
    zip_safe=False,
    install_requires=requirements,
    classifiers=[
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "Natural Language :: English",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.9",
    ],
    packages=setuptools.find_packages(),
    package_dir={app_name: app_name},
    include_package_data=True,
  )
