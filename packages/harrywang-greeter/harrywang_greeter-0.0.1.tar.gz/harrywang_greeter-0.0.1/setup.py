import os.path
from setuptools import setup

# file directory
HERE = os.path.abspath(os.path.dirname(__file__))

# README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(name='harrywang_greeter',
      version='0.0.1',
      description='A minimal PyPI package',
      long_description=README,
      long_description_content_type="text/markdown",
      url='https://github.com/harrywang/greeter-python',
      author='Harry Wang',
      author_email='harryjwang@gmail.com',
      license='MIT',
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
      ],
      packages=['harrywang_greeter'],
)