from setuptools import setup
from pathlib import Path

VERSION = '0.0.11'
DESCRIPTION = 'PyElectroSim é uma biblioteca para simulação da trajetória de cargas elétricas em um sistema de coordenadas cartesianas.'
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

setup(
    name="PyElectroSim",
    version=VERSION,
    author="Robson-tech",
    author_email="robson.junior@ufpi.edu.br",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["PyElectroSim"],
    install_requires=['pygame'],
)