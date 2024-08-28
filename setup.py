from setuptools import setup

with open("README.md","r", encoding="utf-8") as fh:
    long_descciption = fh.read()

Author_name = "Dibyansu Mishra"
SRC_REPO = 'src'
LIST_OF_REQUIRMENTS = ['streamlit']

setup(
    name = SRC_REPO,
    version = '0.0.1',
    author = Author_name,
    euthor_email = "dibyansu.mishra2003@gmail.com",
    description= 'A small example package for movies recommendations.',
    long_description= long_descciption,
    long_description_content_type= 'text/markdown',
    package = [SRC_REPO],
    python_requires = '>=3.7',
    install_requires = LIST_OF_REQUIRMENTS
)
    