import setuptools
import pkgutil
import sys

install_requires = []

if sys.version_info < (3, 7):
    install_requires.append('pyside2')
else:
    if not pkgutil.find_loader('PySide2'):
        install_requires.append('pyside6')

setuptools.setup(
    name="isTrue",
    version="0.0.10",
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
    install_requires=install_requires
)
