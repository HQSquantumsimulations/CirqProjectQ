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

print("Warning: CirqProjectQ is no longer actively maintained, package only available for legacy purposes")

setup(name='CirqProjectQ',
      description=('PACKAGE NO LONGER ACTIVELY MAINTAINED Provides: ProjectQ decompositions from common gates to native cirq Xmon gates;'
                   +'  ProjectQ backend to convert a ProjectQ algorithm to a cirq.Circuit'),
      version='0.2.3',
      long_description=readme,
      packages=find_packages(exclude=('docs')),
      author='HQS Quantum Simulations',
      author_email='info@quantumsimulations.de',
      url='https://github.com/HQSquantumsimulations/CirqProjectQ',
      download_url='https://github.com/HQSquantumsimulations/CirqProjectQ/archive/v0.2.3.tar.gz',
      license=license,
      install_requires=install_requires
      )
