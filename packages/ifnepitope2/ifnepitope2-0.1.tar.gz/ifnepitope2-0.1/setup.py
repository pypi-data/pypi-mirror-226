from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ifnepitope2',
    version='0.1',
    description='A tool to predict ifn inducing epitopes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/ifnepitope2', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'ifnepitope2.blast_binaries':['**/*'], 
    'ifnepitope2.blast_db':['**/*'],
    'ifnepitope2.model':['*']},
    entry_points={ 'console_scripts' : ['ifnepitope2 = ifnepitope2.python_scripts.ifnepitope2:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas', 'tqdm',  # Add any Python dependencies here
    ]
)
