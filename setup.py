from setuptools import setup, find_packages


def _read_requirements(file):
    with open(file) as f:
        requirements = f.read().splitlines()
    return requirements


requirements = _read_requirements("requirements_deploy.txt")

setup(
    name="temporun",
    version="0.1",
    author="Gerard Hager",
    author_email="ghager93@gmail.com",
    license="MIT License",
    packages=find_packages(exclude=["test", "detection_methods"]),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "temporun = app.main:app"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ]
)