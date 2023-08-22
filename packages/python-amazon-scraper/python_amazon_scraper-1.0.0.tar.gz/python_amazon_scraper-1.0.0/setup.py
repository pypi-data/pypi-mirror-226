from setuptools import setup, find_packages
import pathlib

base = pathlib.Path(__file__).parent.resolve()
# Get the long description from the README file
long_description = (base / "README.md").read_text(encoding="utf-8")

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  "Topic :: Software Development :: Libraries :: Python Modules",
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  "Programming Language :: Python :: 3.7",
  "Programming Language :: Python :: 3.8",
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
]
 
setup(
  name='python_amazon_scraper',
  version='1.0.0',
  description='Scrap Product Data from Amazon',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://github.com/sannjayy/python_amazon_scraper',  
  author='Sanjay Sikdar',
  author_email='me@sanjaysikdar.dev',
  license='MIT', 
  classifiers=classifiers,
  keywords='python, scraper, amazon scraper', 
  packages=find_packages(where="src"),
  python_requires=">=3.9, <4",   
  package_dir={'':'src'},
  install_requires=[
    'beautifulsoup4==4.12.2',
    'lxml==4.9.3',
    'requests==2.31.0',
  ],
  project_urls={
    "Bug Reports": "https://github.com/sannjayy/python_amazon_scraper/issues",
    "Funding": "https://www.paypal.com/paypalme/znasofficial",
    "Say Thanks!": "https://saythanks.io/to/sannjayy",
    "Source": "https://github.com/sannjayy/python_amazon_scraper/",
  },
)