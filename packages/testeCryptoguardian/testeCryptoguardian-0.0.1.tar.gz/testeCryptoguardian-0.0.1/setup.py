from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Uma ferramenta de criptografia e descriptografia de arquivos.'
with open('README.md', 'r', encoding='utf-8') as long_description_file:
    LONG_DESCRIPTION = long_description_file.read()

setup(
    name = 'testeCryptoguardian',
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    author = 'Melissa Alves e Davi Rodolfo',
    author_email = 'msnmelissaoa15@hotmail.com',
    packages = ['testeCryptoguardian'],
    install_requires = [
        'cryptography'
    ],

    classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent"
    ]
)