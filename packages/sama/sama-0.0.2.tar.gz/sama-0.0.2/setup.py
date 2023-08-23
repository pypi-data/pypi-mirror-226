from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='sama',
        version='0.0.2',
        description='Sama Python Client',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://www.sama.com',
        author='Edward',
        author_email='echan@samasource.org',
        license='MIT',
        packages=['sama'],
        install_requires=[
            'retry'
        ])