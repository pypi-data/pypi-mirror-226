from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='algpred2',
    version='1.3',
    description='A tool to predict allergenic proteins and mapping of IgE epitopes ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/algpred2', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'algpred2.blast_binaries':['**/*'], 
    'algpred2.blast_db':['*'],
    'algpred2.model':['*'],
    'algpred2.motif':['*'],
    'algpred2.progs':['*']},
    entry_points={ 'console_scripts' : ['algpred2 = algpred2.python_scripts.algpred2:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas',  'argparse' # Add any Python dependencies here
    ]
)
