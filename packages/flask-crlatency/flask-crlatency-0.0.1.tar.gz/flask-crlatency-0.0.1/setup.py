import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="flask-crlatency",
    version="0.0.1",
    author="Prince Roshan",
    author_email="princekrroshan01@gmail.com",
    url="https://github.com/Agent-Hellboy/flask-crlatency",
    description=(
        "A flask extension to log route latency "
    ),
    long_description=read("README.rst"),
    license="MIT",
    nstall_requires=["flask"],
    package_dir={'': 'src'},
    packages=['flask_crlatency'],
    keywords=[
        "flask-extension","log-route-latency"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)