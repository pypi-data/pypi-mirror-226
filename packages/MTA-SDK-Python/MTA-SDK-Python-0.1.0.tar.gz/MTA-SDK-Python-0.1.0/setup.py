from setuptools import setup

from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='MTA-SDK-Python',
    version='0.1.0',
    license='MIT License',
    author='Lucas Camargo de Andrade',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='lucas.camargo.de.andrade15@gmail.com',
    keywords='MTA SDK Python',
    description=u'A Python SDK To MTA',
    packages=['mtasdk'],
    install_requires=['requests'],)