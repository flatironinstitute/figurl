from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    scripts=[],
    include_package_data = True,
    package_data={
        'figurl': ['preserve/templates/*']
    },
    install_requires=[
        'click',
        'altair',
        'kachery>=2.0.1'
    ],
    entry_points={
        "console_scripts": [
            "figurl=figurl.cli:main",
        ],
    }
)
