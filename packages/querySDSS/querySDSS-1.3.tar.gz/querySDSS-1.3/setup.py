import setuptools


setuptools.setup(
    name='querySDSS',
    version='1.3',
    license='MIT',
    author="aCosmicDebbuger",
    author_email='acosmicdebugger@gmail.com',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/aCosmicDebugger/querySDSS',
    keywords='example project',
    install_requires=[
          'astropy', 'astroquery',
      ],

)
