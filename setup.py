from setuptools import setup, find_packages

setup(
    name="picrosolve",
    version="0.1",
    packages=find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },
    entry_points={
        "console_scripts": [
            "picrosolve = picrosolve:main",
        ]
    },

    # metadata for upload to PyPI
    author="julian",
    author_email="julian.naydichev@gmail.com",
    description="I just wanted a picross thing in python",
    license="??",
    keywords="picross",
    url="",   # project home page, if any
)
