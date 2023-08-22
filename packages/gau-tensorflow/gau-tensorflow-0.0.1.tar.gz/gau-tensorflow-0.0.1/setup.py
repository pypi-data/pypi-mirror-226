from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Tensorflow implementation of Gated Attention Unit'
LONG_DESCRIPTION = 'A package that containts a Tensorflow implementation of Gated Attention Unit'

# Setting up
setup(
    name="gau-tensorflow",
    version=VERSION,
    author="kevinyecs",
    author_email="<kevinyecodes@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['tensorflow'],
    keywords=['python', 'gau', 'ml', 'tensorflow', 'gated attention unit', 'transformer'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)