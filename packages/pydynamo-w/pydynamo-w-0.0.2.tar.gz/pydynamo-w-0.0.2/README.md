# Pydynamo-w
Pydynamo-w is a module to define, run and analyse system dynamics. I first present how to use the practical session we designed to play with the module, and then brief comments and references in english at the end.

# Comments in english   
It was originally created to run the World3 model [2], written in DYNAMO language [1]. Included in the module are functions to convert DYNAMO code to pydynamo syntax. All scenarios of *Limits to Growth*, updated with 2003 version, are shown in [LimitsToGrowth03](./examples/LimitsToGrowth03.ipynb). For a quick tuto of how to use World3 in pydynamo, see [World3](./examples/World3.ipynb). For a quick tuto on how to use pydynamo, see [BTmodel](./examples/BTmodel.ipynb).

Documentation about the World models is in <https://abaucher.gitlabpages.inria.fr/pydynamo/>.

## Installation
- clone this repository and got to folder
- python -m pip install -r requirements.txt
- you can import pydynamo

## Note
_This is a beta version and all documentation and commands may not be complete or updated_

## Usage
- Define the system equations in a function or file with pydynamo syntax
- Get a System object from this function or file
- Run, change parameters, re-run, plot

## Author
Achille BAUCHER for my internship at the LIG-lab. I used some functions from pyworld3 [3], and nice explanations by it's author Charles Vanwynsberghe.

## References
- [1] How DYNAMO  works: <https://archive.org/details/dynamousersmanua0000pugh/>
  - Some additional explanations about DYNAMO language are in [dynamo_doc](./dynamo_doc.md)
- [2] Book describing the world3 model: <https://archive.org/details/dynamicsofgrowth0000unse/>
- [3] Pyworld3: <https://github.com/cvanwynsberghe/pyworld3>
