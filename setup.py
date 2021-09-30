from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="airshare",
    version="0.0.1",
    description="airshare is a Python peer-to-peer network application to share clipboard between multiple computers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kamodulin/airshare",
    author="Kamran Ahmed",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
