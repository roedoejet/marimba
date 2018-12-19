from setuptools import setup, find_packages
import marimba

setup(
    name='marimba',
    version=marimba.VERSION,
    long_description='marimba',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask']
)