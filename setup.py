from setuptools import setup
import os.path

current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, 'README.md')) as rdr:
    long_description = rdr.read()

setup(name='libtrace',
      version='0.1.0',
      description='Library for tracing events',
      long_description=long_description,
      url='http://github.com/adamvinueza/libtrace',
      author='Adam Vinueza',
      author_email='adamvinueza@pm.me',
      license='Apache 2.0',
      packages=['libtrace'],
      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
      ],
      zip_safe=False)
