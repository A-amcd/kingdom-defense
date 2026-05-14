from setuptools import setup

setup(
    name='kingdomdefense',
    version='0.1.0',
    scripts=['main.py'],
    install_requires=[
        'pygame',
    ],
    include_package_data=True,
    zip_safe=False,
)