from setuptools import setup, find_packages

setup(
    name="unigridchain-cli",
    version="0.0.1",
    url="https://github.com/unigrid-project/unigridchain-cli",
    author="UGD Software AB",
    author_email='info@unigrid.org',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'unigridchain-cli=unigridchain.cli:cli',
        ],
    },
)
