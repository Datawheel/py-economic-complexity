# Economic Complexity calculations

Economic Complexity studies the geography and dynamics of economic activities using methods inspired in ideas from complex systems, networks, and computer science.

This package allows to calculate Economic Complexity measures. For further references about methodology and implicances of Economic Complexity itself, you can visit the Observatory of Economic Complexity at [oec.world](https://oec.world/en/resources/methods#economic-complexity).

We also have [a brief Tutorial](./docs/TUTORIAL.ipynb), using data from the OEC, to get started on how to use the basic functions of this package.

<a href="https://github.com/Datawheel/py-economic-complexity/blob/main/LICENSE">
  <img src="https://flat.badgen.net/github/license/Datawheel/py-economic-complexity" />
</a>
<a href="https://github.com/Datawheel/py-economic-complexity/issues">
  <img src="https://flat.badgen.net/github/issues/Datawheel/py-economic-complexity" />
</a>
<a href="https://pypi.org/project/economic-complexity/">
  <img src="https://flat.badgen.net/pypi/v/economic-complexity" />
</a>

## Usage

This package contain the following functions:

* RCA:
  - `rca`
* Economic/Product Complexity:
  - `complexity`
  - `complexity_subnational`
* Product-space:
  - `distance`
  - `opportunity_gain`
  - `proximity`
  - `relatedness`
  - `similarity`
  - `pgi`
  - `peii`
* Cross-space:
  - `cross_proximity`
  - `cross_relatedness`

Each module is documented by docstring. Write in your python IDLE the module's name and question symbol to read the documentation.
> ex. if you import the complexity package as `import economic_complexity as ecplx` then the command `ecplx.rca?` shows you the information about rca module)

## Installation

The `pyproject.toml` file in this repository contains settings to use with [`poetry`](https://python-poetry.org/). You can generate an installable wheel file using the `build` command:

```bash
$ poetry build --format wheel
```

The package is also available on pypi.org, under the name `economic-complexity`. You can install it using `poetry` or `pip`.

```bash
$ poetry install economic-complexity
```
```bash
$ pip install economic-complexity
```

## Development

After cloning the repo, install the dependencies with the command:

```bash
$ poetry install
```

## References

* Hidalgo, César A. (2021). Economic complexity theory and applications. _Nature Reviews Physics, 3_(2), 92–113. https://doi.org/10.1038/s42254-020-00275-1

* Catalán, P., Navarrete, C., & Figueroa, F. (2020). The scientific and technological cross-space: Is technological diversification driven by scientific endogenous capacity? _Research Policy, 104016_, 104016. https://doi.org/10.1016/j.respol.2020.104016

* Hidalgo, César A., & Hausmann, R. (2009). The building blocks of economic complexity. _Proceedings of the National Academy of Sciences of the United States of America, 106_(26), 10570–10575. https://doi.org/10.1073/pnas.0900943106

* Hidalgo, C. A., Klinger, B., Barabási, A.-L., & Hausmann, R. (2007). The product space conditions the development of nations. _Science (New York, N.Y.), 317_(5837), 482–487. https://doi.org/10.1126/science.1144581

* Hartmann, D., Guevara, M. R., Jara-Figueroa, C., Aristarán, M., & Hidalgo, C. A. (2017). Linking Economic Complexity, Institutions, and Income Inequality. _World Development_, 93, 75–93. https://doi.org/10.1016/j.worlddev.2016.12.020

* Romero, J. P., & Gramkow, C. (2021). Economic complexity and greenhouse gas emissions. _World Development_, 139, 105317. https://doi.org/10.1016/j.worlddev.2020.105317

* Bahar, D., Hausmann, R., Hidalgo, C. A. (2014). Neighbors and the evolution of the comparative advantage of nations: Evidence of international knowledge diffusion?. _Journal of International Economics_, 92, 111-123. http://dx.doi.org/10.1016/j.jinteco.2013.11.001


---
&copy; 2022 [Datawheel, LLC.](https://www.datawheel.us/)  
This project is licensed under [MIT](./LICENSE).
