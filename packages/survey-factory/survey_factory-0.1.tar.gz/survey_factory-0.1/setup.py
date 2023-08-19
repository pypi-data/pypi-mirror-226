from setuptools import setup, find_packages

setup(
    name='survey_factory',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    author='Chatrli',
    author_email='chatrli@proton.me',
    description='A factory for generating mock survey data to train machine learning models.',
    license='CC0 1.0 Universal',
    url='https://github.com/chatrli/survey_factory',
)
