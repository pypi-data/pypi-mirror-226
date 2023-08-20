from setuptools import setup

setup(
    name = "detectron2_layers",
    version = "0.0.5",
    author = "Andrew Healey",
    author_email = "doolie.healey@gmail.com",
    description = ("A replacement for detectron2.layers, specifically for use by SegGPT."),
    license = "Apache",
    packages=['detectron2_layers'],
    install_requires=[
        'fvcore',
        'torch',
    ]
)