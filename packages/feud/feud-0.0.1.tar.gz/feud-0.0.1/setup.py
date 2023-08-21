from setuptools import setup, find_packages

VERSION = '0.0.1' 

setup(
    name="feud", 
    version=VERSION,
    author="Edwin Onuonga",
    author_email="ed@eonu.net",
    description="Reserved",
    package_dir={"": "lib"},
    packages=find_packages(where="lib"),
)
