# setup.py

from setuptools import setup, find_packages

setup(
    name='hdr-local-processing',
    version='0.1.1',
    url='https://github.com/Elessar11777',
    author='Elessar11777',
    author_email='Elessar11777@gmail.com',
    description='Petri Local Tonemapping Package',
    long_description="None",
    long_description_content_type='text/markdown',
    packages=find_packages(include=['hdrlocal']),
    license="GPL",
    install_requires=[
        "numpy",
        "opencv-python"
    ],
)