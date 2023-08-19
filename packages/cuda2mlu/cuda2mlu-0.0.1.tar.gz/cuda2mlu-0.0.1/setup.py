from setuptools import setup
import site
import os

setup(
    name="cuda2mlu",
    version="0.0.1",
    description="rewrites torch CUDA device to use MLU",
    long_description = "A package that rewrites torch device CUDA to use MLU",
    packages=["cuda2mlu"],
    install_requires=["torch"],
    setup_requires=["torch"],
    entry_points={
        'console_scripts': [
            'cuda2mlu = cuda2mlu:cmd',
        ]
    },
    python_requires=">=3.6"
)

