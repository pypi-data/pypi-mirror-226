import setuptools


setuptools.setup(
    name="isTrue",
    version="0.0.8",
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
    extras_require={
        'pyside2': 'PySide2',
        'pyside6': 'PySide6'}
)
