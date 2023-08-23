from setuptools import setup, find_packages

"""
pip install twine
python setup.py sdist --formats=zip
python -m twine upload  dist* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDVjNWQ5MzRhLTQ5Y2EtNDYzMC1hZWU5LWUzOGU1NzIxNmI5ZQACKlszLCJhNDk0MTc0YS01YmFjLTQ1NDQtOThkNi1jOWVlODJkY2UzNzgiXQAABiCS4uKhxv-GWwk0SD_3JUx5SWSbzZ3lyfuR0v1WwQ4fcg
"""

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='simplybk',
    version='2',
    packages=find_packages(),
    url='https://github.com/',
    author='Hamdy Khader',
    author_email='hamdy.khader@gmail.com',
    description='CLI for managing SimplyBlock cluster',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "foundationdb",
        "requests",
        "typing",
        "prettytable",
        "docker",
        "psutil",
    ],
    entry_points={
        'console_scripts': [
            'simplybk=management.cli:main',
        ]
    },
    include_package_data=True,
    package_data={'': ['scripts/*.*', 'services/*.*', 'spdk_installer/*.*']},
)
