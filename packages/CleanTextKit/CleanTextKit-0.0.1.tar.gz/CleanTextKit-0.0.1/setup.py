from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='CleanTextKit',
    version='0.0.1',
    description='A preprocessor which performs operations of lowering text, removing special characters and removing stopwords',
    author= 'Chaitanya Kulkarni',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['text processing', 'text preprocessing', 'text cleaner'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['TextPreProcessor'],
    package_dir={'':'src'},
    install_requires = [
        'nltk'
    ]
)
