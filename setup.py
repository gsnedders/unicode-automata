import os

from setuptools import find_packages, setup


base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()


setup(
    name="uautomata",
    version="0.1",
    description="Automata library designed for Unicode",
    long_description=long_description,
    license="Apache 2.0",
    url="XXX",
    author="Geoffrey Sneddon",
    author_email="me@gsnedders.com",

    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=True,

    install_requires=[
        "intervaltree>=2.1.0,<3",
    ],

    tests_require=[
        "pytest>=3.3.0,<4",
    ],

    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent"
    ]
)
