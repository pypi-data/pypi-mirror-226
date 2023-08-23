from setuptools import setup, find_packages

VERSION = '0.1.2'
DESCRIPTION = 'Pacote gerador e decodificador de QR CODE'
with open("README.md", "r", encoding="utf-8") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

#setting up
setup(
    name="qrcode_utils",
    version=VERSION,
    author="Sheila Paloma de Sousa Brito",
    author_email="sheila.psb@gmail.com.br",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=['opencv-python', 'qrcode', 'numpy']
)