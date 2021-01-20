# dev-complexity-package

package which host a set of function to compute complexity.  

## compile the package
first install the **setuptools** and **wheel** packages

```sh
python3 -m pip install --user --upgrade setuptools wheel
```

next compile the package 
```sh
python3 setup.py sdist bdist_wheel
```

Now we have two new folders in our directory **dist** and **complexity_pkg.egg-info**. **dist** folder contains a **.whl** file that is our compiled package.

## install package 
to install the package we have to run the follwing command:

```sh
pip install **some-package**.whl
```

## test

tests have not been created.

## reference 
https://packaging.python.org/tutorials/packaging-projects/