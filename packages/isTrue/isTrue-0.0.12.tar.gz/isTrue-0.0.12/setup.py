import setuptools
import pkg_resources
import sys

install_requires = []

if sys.version_info < (3, 7):
    install_requires.append('pyside2')
    print("Adding pyside2 to requirements.")
else:
    if "pyside2" not in [i.key for i in pkg_resources.working_set]:
        print("pyside2 not found")
        print("Adding pyside6 to requirements.")
        install_requires.append('pyside6')

setuptools.setup(
    name="isTrue",
    version="0.0.12",
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
