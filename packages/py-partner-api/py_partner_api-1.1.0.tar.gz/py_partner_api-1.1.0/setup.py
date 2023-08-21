from setuptools import setup, find_packages

readme = ""
license = ""

with open("README.md", "r") as fh:
    readme = fh.read()
with open("LICENCE", "r") as fh:
    license = fh.read()
 
setup(
    name = "py_partner_api",
    version = "1.1.0",
    keywords = ("partner", "smm"),
    description = "Simple work with partner",
    long_description = readme,
    license = license,
    url = "",
    author = "DPhascow",
    author_email = "d.sinisterpsychologist@gmail.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests", "beautifulsoup4",]
)