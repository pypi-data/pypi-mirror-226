from setuptools import setup, find_packages
from src.package_info import __version__, __package_name__

setup(
    name=__package_name__,
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'certifi',
        'websockets',
        'packaging'
    ],
    entry_points={
        'console_scripts': [
            'urt=src.launcher:main',
        ],
    }
)
