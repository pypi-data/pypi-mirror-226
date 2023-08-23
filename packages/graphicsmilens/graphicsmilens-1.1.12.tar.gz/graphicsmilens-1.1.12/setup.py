from setuptools import setup, find_packages

VERSION = '1.1.12'
DESCRIPTION = 'Pacote gerador de gráficos'
with open("README.md", "r", encoding="utf-8") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

# setting up
setup(
    name="graphicsmilens",
    version=VERSION,
    author="Milene Fialho",
    author_email="milefialho16@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=['matplotlib', 'pandas'],
)
