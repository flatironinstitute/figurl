from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    scripts=[],
    include_package_data = True,
    install_requires=[
        'click',
        'altair',
        'kachery_cloud'
    ]
)
