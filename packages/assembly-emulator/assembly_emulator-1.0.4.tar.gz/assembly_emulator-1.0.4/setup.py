import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="assembly_emulator",
    version="1.0.4",
    description="Emulate basic Lisp environment in python3 for educational reasons.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="jonaprojects",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["assembly_emulator"],
    include_package_data=True,
    install_requires=["pyfiglet"],
)
