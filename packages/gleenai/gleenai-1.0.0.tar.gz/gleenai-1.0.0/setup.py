# setup.py

from setuptools import setup, find_packages

setup(
    name="gleenai",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author="Nagendra Kumar",
    author_email="nagendra@helix3.io",
    description="Python wrapper for GleenAI API.",
    license="MIT",
    keywords="gleenai api wrapper",
)

