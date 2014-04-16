# Setup file to distribute isotopomer package using distutils.
from distutils.core import setup

prj = 'plotarray'

setup(name=prj,
      version='1.0',
      description='Package to make arrays of plots using matplotlib.',
      author='David Schryer',
      author_email='schryer@ut.ee',
      url='http://www.tuit.ut.ee/',
      packages=[prj],
      )
