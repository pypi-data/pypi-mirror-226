from setuptools import setup

setup(
    name='fatoora_einvoice',
    version='1.1.0',
    description='Digitally Signing Xml using private key certificate invoice and get Qrcdoe invoice hash for zatca phase2, '
                'It is takes informations and parameters from the user and returns the singed xml in base64 ready to submit to zatca',
    author='Muhammad Bilal',
    author_email='bilaljmal@gmail.com',
    url='https://github.com/bilaljmal/fatoora_einvoice',
    packages=['fatoora_einvoice_zatca_phase2'],
    install_requires=['jpype1'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)