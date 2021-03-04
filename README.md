# Complexity package by Datawheel
Economic Complexity studies the geography and dynamics of economic activities using methods inspired in ideas from complex systems, networks, and computer science.

This package allows to calculate Economic Complexity measures. For further references about methodology and implicances of Economic Complexity itself, you can visit [oec.world](https://oec.world/en/resources/methods#economic-complexity).

## Requirement 
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

## package functions
the package contain the follwing modules

* rca
* complexity
* proximity
* relatedness
* distance
* opportunity_gain
* cross_proximity
* cross_relatedness

each module is documented by docstring. Write in your python IDLE the module's name and question symbol to read the documentation.
> ex. if you import the complexity package as `import complexity as cmplx` then the command `cmplx.rca?` shows you the information about rca module)

## Brief Tutorial 

In this section we are going to development a brief example to show you how use this package to obtain a ECI ranking using data from [oec.world](oec.world). 

> Our goal will be to reproduce the ECI ranking using 2018 exports data classified according the Harmonized System (HS92) with a depth of 4 Digits for countries with population of at least 1 million and exports of at least $1 billion, and products with world trade over 500 million. (for more details see [link](https://oec.world/en/resources/methods))

Let us start to call some packages, including the complexity package (that we will call `cmplx`)
```py
import pandas as pd
import numpy as np
import requests
import complexity as cmplx
```

We will use the following function to simplify the data request from the OEC.
```py
def request_data(url):
    data = requests.get(url)
    data = data.json()
    df = pd.json_normalize(data['data'])
    return df
```

Now, we fetch the data. In this case we gather the trade data and population using the OEC API.

```py
url_trade = 'https://dev.oec.world/olap-proxy/data.jsonrecords?Year=2016,2017,2018&cube=trade_i_baci_a_92&drilldowns=Exporter+Country%2CHS4&measures=Trade+Value'

df_trade = request_data(url_path)

url_wdi = 'https://dev.oec.world/olap-proxy/data.jsonrecords?Indicator=SP.POP.TOTL&Year=2018&cube=indicators_i_wdi_a&drilldowns=Country&measures=Measure'

df_wdi = request_data(url_wdi)
```

Next, filter the data. This is necessary to make the calculations properly. 
```py
df = df_trade.copy()
df_population = df_wdi[df_wdi['Measure']>1000000]

df_products = df.groupby('HS4 ID')['Trade Value'].sum().reset_index()
df_products = df_products[df_products['Trade Value']>3*500000000]

df_countries = df.groupby('Country ID')['Trade Value'].sum().reset_index()
df_countries = df_countries[df_countries['Trade Value']>3*1000000000]

df_filter  = df[#(df['Country ID'].isin(df_countries['Country ID'])) & 
               (df['Country ID'].isin(df_population['Country ID'])) &
               (df['HS4 ID'].isin(df_products['HS4 ID']))]
```

Formating the data to compute the RCA matrix and the ECI. 
> the RCA module receive a pivot table as argument, where countries ids are the index and product ids the columns.
```py
df_pivot = pd.pivot_table(df_filter, index=['Country ID'], columns=['HS4 ID'],values='Trade Value').reset_index().set_index('Country ID').dropna(axis=1, how="all").fillna(0).astype(float)
```

Compute the RCA matrix, ECI and PCI.
```py
rca = cmplx.rca(df_pivot)
ECI,PCI = cmplx.complexity(rca)
```

sort the ECI list to create your ranking and compare with the info in the [oec.world](https://oec.world/en/rankings/eci/hs4/hs92).
```py 
ECI.sort_values(ascending=False)
```