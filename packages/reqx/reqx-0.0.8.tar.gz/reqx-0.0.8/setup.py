from setuptools import find_packages, setup
from pathlib import Path

cwd = Path.cwd()
about = {}
exec((cwd / 'reqx' / '__version__.py').read_text(), about)

install_requires = [
    'httpx[http2]',
    'uvloop; platform_system != "Windows"',
    'nest-asyncio',
    'aiofiles',
    'tqdm',
    'orjson',
    'selectolax',
]

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    description=about['__description__'],
    license=about['__license__'],
    long_description=(cwd / 'README.md').read_text(),
    python_requires=">=3.10.10",
    long_description_content_type='text/markdown',
    author_email='trevorhobenshield@gmail.com',
    url='https://github.com/trevorhobenshield/reqx',
    install_requires=install_requires,
    keywords='http networking async concurrency efficient webscraping scraping scraper automation',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
