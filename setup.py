from setuptools import find_packages, setup

with open('README.md') as file:
    readme = file.read()

with open('LICENSE') as file:
    license = file.read()

install_requires = [
		'cirq',
		'projectq',
    		'numpy',
    		'pytest',
]

setup(name='CirqProjectQ',
      description='',
      version='0.0.1',
      long_description=readme,
      packages=find_packages(exclude=('docs')),
      author='Heisenberg Quantum Simulations',
      author_email='info@heisenberg.xyz',
      url='heisenberg.xyz',
      download_url='https://github.com/HeisenbergQS/CirqProjectQ/archive/v0.0.1.tar.gz',
      license=license,
      install_requires=install_requires
      )
