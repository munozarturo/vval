from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="vval",
    version="2.1.1",
    author="Arturo Munoz",
    author_email="munoz.arturoroman@gmail.com",
    description="Input validation in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/munozarturo/vval",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="http, requests, wrapper, retry, timeout",
    python_requires=">=3.11",
    install_requires=["varname==0.11.0", "typing_inspect==0.8.0"],
    extras_require={
        "dev": ["pytest", "pytest-cov", "flake8", "black"],
        "docs": ["sphinx", "sphinx_rtd_theme"],
    },
    project_urls={
        "Bug Reports": "https://github.com/munozarturo/wreqs/issues",
        "Source": "https://github.com/munozarturo/wreqs/",
    },
)
