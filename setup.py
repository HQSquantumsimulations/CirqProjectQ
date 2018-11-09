from setuptools import find_packages, setup

with open('README.md') as file:
    readme = file.read()

with open('LICENSE') as file:
    license = file.read()

install_requires = [
		'cirq',
		'projectq',
    'cmath',
    'numpy',
    'pytest',
]

setup(name='CirqProjecQ',
      description='',
      version='0.0.1',
      long_description=readme,
      packages=find_packages(exclude=('docs')),
      author='Heisenberg Quantum Simulations',
      author_email='info@heisenberg.xyz',
      url='heisenberg.xyz',
      license=license,
      install_requires=install_requires
      )
