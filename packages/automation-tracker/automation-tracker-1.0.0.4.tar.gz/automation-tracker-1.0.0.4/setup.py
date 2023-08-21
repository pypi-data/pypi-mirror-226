from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0.4'
DESCRIPTION = 'Robot Framework Library for Tracking Test Cases'
LONG_DESCRIPTION = 'A package that allows you to track test cases in Robot Framework'

# Setting up
setup(
    name="automation-tracker",
    version=VERSION,
    author="Justus Mwangi",
    author_email="<mwangijustus12@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['robotframework','requests','robotframework-requests', 'robotframework-jsonlibrary',
                      'robotframework-listenerlibrary','robotframework-seleniumlibrary','urllib3','robotframework-stringformat' ],
    keywords=['python', 'robotframework', 'robotframework-library', 'robotframework-library',
              'robotframework-tracking', 'robotframework-tracker', 'robotframework-tracker', 'robotframework-tracker'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
