from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install tplib
    #
    # And where it will live on PyPI: https://pypi.org/project/tplib/
    #
    name="tplib",
    version="1.0.0",
    description="A python library for managing test cases, test plans",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://github.com/rhinstaller/tplib",
    author="Pavel Holica",
    author_email="pholica@redhat.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="testcases, testplans, yaml",
    package_dir={"": "."},
    packages=find_packages(where="."),
    python_requires=">=3, <4",
    install_requires=[
        'jinja2',
        'pyyaml'
        ],
    package_data={
        "": ["doc/*", "examples/*"],
    },
    entry_points={
        "console_scripts": [
            "tcdiff=tplib.diff_main:main",
            "tc_generate_documents=tplib.generate_documents_main:main",
            "tcquery=tplib.query_main:main",
            "tcvalidate=tplib.validate_main:main",
        ],
    },
)
