from setuptools import setup, find_packages

# Read the content of the README.md file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rtf-converter',
    version='0.1.0',
    packages=find_packages(),
    
    description='Easily convert RTF to plain text format - Supports Javascript, Python, CSharp and PHP.',
    
    long_description=long_description,
    long_description_content_type='text/markdown', 
)