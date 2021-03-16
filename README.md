# Complexity package by Datawheel

Economic Complexity studies the geography and dynamics of economic activities using methods inspired in ideas from complex systems, networks, and computer science.

This package allows to calculate Economic Complexity measures. For further references about methodology and implicances of Economic Complexity itself, you can visit [oec.world](https://oec.world/en/resources/methods#economic-complexity).

## Requirements
> used in the development 
* python 3.8.2
* numpy 1.18.2
* pandas 1.1.1

## Install

After clone the repository, install the **setuptools** and **wheel** packages
```sh
python3 -m pip install --user --upgrade setuptools wheel
```

next compile the package in its directory
```sh
python3 setup.py sdist bdist_wheel
```

Now we have two new folders in our directory **dist** and **complexity_pkg.egg-info**. **dist** folder contains a **.whl** file that is our compiled package which we will install.

To install the package we have to run the follwing command:
```sh
pip install **some-package**.whl
```

## Functions available

This package contain the following modules and functions:

* rca:
  - rca
* complexity:
  - complexity
* product_space:
  - distance
  - opportunity_gain
  - proximity
  - relatedness
* cross_space:
  - cross_proximity
  - cross_relatedness

Each module is documented by docstring. Write in your python IDLE the module's name and question symbol to read the documentation.
> ex. if you import the complexity package as `import complexity as cmplx` then the command `cmplx.rca?` shows you the information about rca module)
