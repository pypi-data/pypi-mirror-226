from setuptools import setup, find_packages

readme = ""
license = ""

with open("README.md", "r") as fh:
    readme = fh.read()
with open("LICENCE", "r") as fh:
    license = fh.read()
 
setup(
    name = "py_remap",
    version = "1.1.0",
    keywords = ("remap", ),
    description = "",
    long_description = readme,
    license = license,
    url = "https://github.com/DephPhascow/py_remap",
    author = "dphascow",
    author_email = "d.sinisterpsychologist@gmail.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [""]
)