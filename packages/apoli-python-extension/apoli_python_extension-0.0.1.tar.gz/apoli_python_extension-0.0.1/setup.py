from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="apoli_python_extension",
    version="0.0.1",
    author="ThatRobin",
    description="A python package that can create Datapacks and Resourcepacks using Apoli powers.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["apoli_python_extension"]
)