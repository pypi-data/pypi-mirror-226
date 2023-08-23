from setuptools import setup

setup(
    name='ImageFetchPy',
    version='0.1',
    description='Python library to download images from a URL',
    author='Raheel Asghar Ghauri',
    author_email='raheelghauri786@hotmail.com',
    packages=['ImageFetchPy'],
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
)
