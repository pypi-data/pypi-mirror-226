from setuptools import setup, find_packages

VERSION = '1.1.9'
DESCRIPTION = 'Pacote gerador de gráficos'
LONG_DESCRIPTION = 'Pacote que contém funções que geram gráficos tipo pizza, linha, ponto, barra'

#setting up
setup(
        #'name' deve corresponder ao nome da pasta 'PacoteTeste'
        name = "graphicsmilens",
        version=VERSION,
        author="Milene Fialho",
        author_email="milefialho16@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license='MIT',
        packages=find_packages(),
        install_requires=['matplotlib','pandas'],# adicione outros pacotes que precisem ser instalados com o seu pacote. EX: 'caer'
        
) 