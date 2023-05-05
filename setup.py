from setuptools import setup, find_packages
from typing import List



with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

def get_requirements()->List[str]:

    with open (REQUIREMENT_FILE_NAME) as requires:
        requirements_list = requires.readlines()
        requirements_list = [x.replace("/n", "") for x in requirements_list]
        if HYPHEN_E_DOT in requirements_list:
            requirements_list.remove(HYPHEN_E_DOT)
        return requirements_list


## edit below variables as per your requirements -
REPO_NAME = "NER Project with custom data"
AUTHOR_USER_NAME = "Sushant Sur"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = []
REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_E_DOT = "-e ."


setup(
    name=SRC_REPO,
    version="0.0.1",
    author="Sushant Sur",
    description="A small local packages for NER Implementation with Pytorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sushantsur23/NER_with_custom_data.git",
    author_email="sushant.sur23@gmail.com",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.8",
    install_requires=get_requirements(),
)
