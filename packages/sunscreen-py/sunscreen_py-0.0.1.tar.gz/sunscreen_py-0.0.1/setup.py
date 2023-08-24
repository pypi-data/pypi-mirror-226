from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Sunscreen Python Interop Package"
LONG_DESCRIPTION = "Sunscreen Python Interop Package"

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="sunscreen_py",
    version=VERSION,
    author="SmartFHE",
    author_email="hello@sunscreen.tch",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    include_package_data=True,
    package_dir={"": "source"},
   # packages=find_packages(),
    keywords=["cryptography", "sunscreen", "fhe", "bfv"],
    install_requires=[
        'torch',
        'importlib_resources',
        'importlib_metadata',
    ],
)
