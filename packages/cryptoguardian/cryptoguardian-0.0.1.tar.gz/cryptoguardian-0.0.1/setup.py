from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Uma ferramenta de criptografia e descriptografia de arquivos.'
with open('README.md', 'r', encoding='utf-8') as long_description_file:
    LONG_DESCRIPTION = long_description_file.read()

setup(
    name = 'cryptoguardian',
    version = VERSION,
    description = DESCRIPTION,
    author = 'Melissa Alves e Davi Rodolfo',
    author_email = 'msnmelissaoa15@hotmail.com',
    packages = ['cryptoguardian'],
    install_requires = [
        'cryptography',
        'PyQt5',
    ],

    classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent"
    ],

    entry_points = {
        'console_scripts': [
            'cryptoguardian = cryptoguardian.main:main',
        ],
    },
)