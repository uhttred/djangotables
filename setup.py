import os
import re

from setuptools import setup


def get_version(filename):
    with open(filename, "r") as fp:
        contents = fp.read()
    return re.search(r"__version__ = ['\"]([^'\"]+)['\"]", contents).group(1)

version = get_version(os.path.join("djangotables", "__init__.py"))

with open("README.rst", "r") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", "r") as history_file:
    history = history_file.read()

setup(
    name="djangotables",
    version=version,
    description=(
        "djangotables is a simple library for generating html "
        "tables with Django Framework using model data like django forms."
    ),
    long_description=readme + "\n\n" + history,
    author="Ageu Matheus",
    author_email="ageumatheus1@gmail.com",
    maintainer="Ageu Matheus",
    maintainer_email="ageumatheus1@gmail.com",
    url="https://github.com/AgeuMatheus/djangotables",
    project_urls={
        "Changelog": (
            "https://github.com/AgeuMatheus/djangotables"
            + "/blob/master/HISTORY.rst"
        )
    },
    packages=["djangotables"],
    license="MIT License",
    keywords=["django", "tables", "djangotables"],
    install_requires=["Django>=2.2"],
    python_requires=">=3.5",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
