from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='openpom',
    version='0.1.0',
    description='Open-source Principal Odor Map models for Olfaction',
    author='Aryan Amit Barsainyan',
    author_email='aryan.barsainyan@gmail.com',
    packages=find_packages(),
    install_requires=requirements,
)
