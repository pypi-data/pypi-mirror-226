
from setuptools import setup, find_packages

# List of classifiers for your package
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Security",
    "Topic :: Security :: Cryptography",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
]


setup(
    name='encryptme',                  
    version='2.2.5',                  
    description='A simple encryption library',  
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read() + '\n\n' + open('usage.md').read(),
    long_description_content_type='text/markdown',  
    author='Adjei Collins',          
    author_email='adjeicollins1672@gmail.com', 
    packages=find_packages(),         
    license='MIT',                    
    classifiers=classifiers,         
    keywords='cryptography encryption encrypt message', 
    install_requires=[],            
)