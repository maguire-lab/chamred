import setuptools
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name='chAMReDb',
    version='0.2.1',
    description='Package to find the equivalent antibiotic resistance genes (ARGs) in other databases based on ARG(s) from one AMR determinant database',
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author='Anthony Underwood',
    author_email='anthony.underwood@cgps.group',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'chamredb = chamredb.run_chamredb:main'
        ]
    },
    install_requires=['networkx', 'pronto', 'rich', 'pandas', 'seaborn', 'numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'coverage'],
    classifiers=[ 
        'Development Status :: 4 - Beta', 
        'Intended Audience :: Science/Research', 
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
