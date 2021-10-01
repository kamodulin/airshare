from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    INSTALL_REQUIRES = f.read().splitlines()

setup(
    name="airshare",
    version="0.0.1",
    description=
    "airshare is a Python peer-to-peer network application to share clipboard between multiple computers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kamodulin/airshare",
    author="Kamran Ahmed",
    packages=find_packages(),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
    entry_points={
        "console_scripts": ["airshare=airshare.airshare:main"],
    })
