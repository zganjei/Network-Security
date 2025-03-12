"""
The setup.py file is an essential part of packaging and distributing Python projects. 
It is used by setuptools (or distutils in older Python versions) to define the 
configuration of your project, such as its metadata, dependencies, and more
"""

from setuptools import find_packages, setup
from typing import List

# install all requirements.txt
def get_requirements() -> List[str]:
    """
    This function will return a list of required packages/libraries
    """
    requirement_list:List[str]=[]
    try: 
        with open('requirements.txt','r') as file:
            lines = file.readlines()

            # go thorugh all lines
            for line in lines:
                #remove empty spaces from the line
                requirement = line.strip()
                #ignore empty lines and -e .
                if requirement and requirement!='-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("Not found requirements.txt file")

    return requirement_list

setup(
    name= "NetworkSecurity",
    version='0.0.1',
    author="Zeinab Ganjei",
    author_email="zzganjei@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
