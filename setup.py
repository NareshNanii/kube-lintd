from setuptools import setup, find_packages

setup(
    name="kube-lintd",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'kube-lintd = kube_lintd.cli:main',
        ],
    },
)

