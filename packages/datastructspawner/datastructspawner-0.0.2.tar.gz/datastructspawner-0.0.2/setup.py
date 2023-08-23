from setuptools import setup

VERSION = '0.0.2'
DESCRIPTION = 'Gerador de Estrutura de Dados'
LONG_DESCRIPTION = 'Esse pacote tem o intuito de gerar lista encadeada, arvore binaria de busca e AVL'

with open('README.md', 'r', encoding='utf-8') as arq:
    readme = arq.read()

setup(name='datastructspawner',
    version=VERSION,
    license='MIT License',
    author='Joao Neto e Lindaiely Rodrigues',
    author_email='joaonetoprivado2001@ufpi.edu.br',
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='estrutura de dados',
    description='Gerador de estruturas de dados',
    packages=['datastructspawner'],)