from setuptools import setup, find_packages


setup(
    name='querySDSS',
    version='0.1',
    license='MIT',
    author="aCosmicDebbuger",
    author_email='acosmicdebugger@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/aCosmicDebugger/querySDSS',
    keywords='example project',
    install_requires=[
          'astropy', 'astroquery',
      ],

)
