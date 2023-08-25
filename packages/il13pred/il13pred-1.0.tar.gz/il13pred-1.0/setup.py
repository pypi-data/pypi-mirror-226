from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='il13pred',
    version='1.0',
    description='A tool for for predicting immunoregulatory cytokine IL-13 inducing peptides',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/il13pred', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'il13pred.model':['*'],
                  'il13pred.Data':['*']},
    entry_points={ 'console_scripts' : ['il13pred = il13pred.python_scripts.il13pred:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas',  'argparse', 'xgboost==1.4.0', 'tqdm' # Add any Python dependencies here
    ]
)
