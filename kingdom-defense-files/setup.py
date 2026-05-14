from setuptools import setup, find_packages

setup(
    name='kingdomdefense',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pygame',
    ],
    entry_points={
        'console_scripts': [
            'kingdomdefense=main:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)