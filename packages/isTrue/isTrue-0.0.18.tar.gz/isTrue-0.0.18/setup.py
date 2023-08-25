import subprocess

import setuptools
import pkg_resources
import sys



setuptools.setup(
    name="isTrue",
    version="0.0.18",
    description="IDK???",
    keywords="IDK???",
    packages=setuptools.find_packages(),
    python_requires='>=3.4',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "License :: Free To Use But Restricted",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",

    ],
    data_files=[("", ["LICENSE.txt", "README.md"])],
)
