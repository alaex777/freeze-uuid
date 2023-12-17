from setuptools import setup, find_packages

setup(
    name='freeze-uuid',
    version='0.1.0',
    author='Alexander Balashov',
    author_email='alaex777@gmail.com',
    description='Python package for mocking uuid.',
    long_description=open('README.md').read(),
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
