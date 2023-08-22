from setuptools import setup

"""
:author: Elieren
"""

version = '1.0.4'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yanimage',
    version=version,

    author='Elieren',
    author_email='kir102906@gmail.com',

    description=(
        u'Python module for searching, getting links and downloading images from Yandex images'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    packages=['yanimage']
)
