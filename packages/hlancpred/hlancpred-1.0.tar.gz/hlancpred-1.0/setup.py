from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='hlancpred',
    version='1.0',
    description='A tool for predicting and scanning the peptides with the ability to bind non-classical class-I HLA alleles',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/hlancpred', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'hlancpred.Models':['*']},
    entry_points={ 'console_scripts' : ['hlancpred = hlancpred.python_scripts.hlancpred:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas',  'argparse', 'xgboost==1.4.0', 'tqdm' # Add any Python dependencies here
    ]
)
