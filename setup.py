from setuptools import setup

setup(
    name="vval",
    version="2.0.1",
    author="Arturo Munoz",
    author_email="munoz.arturoroman@gmail.com",
    description="Input validation in Python",
    long_description="""\
        This package provides a simple way to validate user input in Python.
    """,
    long_description_content_type="text/markdown",
    url="https://github.com/munozarturo/vval",
    packages=["vval"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=["varname==0.11.0", "typing_inspect==0.8.0"],
)
