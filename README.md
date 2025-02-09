# VisualLie

VisualLie is a web app that visualizes the root system of the Feingold-Frenkel
algebra. It uses the Bokeh Python library to generate an interactive 2d plot of
the root system. A 3d plot is generated using the Plotly Python library.
The plots are embedded in a web page providing detailed explanations of all 
their properties.

The VisualLie web app is available at

https://hmalcha.github.io/VisualLie/

For a local version of VisualLie download the
**index.html** file from the docs/ directory and open with your favorite web
browser.

## Getting Started
If you want to modify VisualLie or build the **index.html** file yourself,
follow these steps. 

VisualLie requires a Python installation with
[Bokeh](https://docs.bokeh.org/en/latest/index.html)
and
[Plotly](https://plotly.com/python/)
To install these packages using `pip`, enter

```
pip install bokeh plotly
```

In particular, bokeh will automatically install
[NumPy](https://numpy.org/),
[Pandas](https://pandas.pydata.org/),
and
[Jinja](https://palletsprojects.com/projects/jinja/).
These packages are are also needed for VisualLie.

Then you can run **VisualLie.py** to build **index.html** using

```
python VisualLie.py
```

The **index.html** file is automatically stored in the
docs/ directory.

## Usage
VisualLie is self-contained. When you visit
https://hmalcha.github.io/VisualLie/
or open the **index.html** file you are presented with a detailed
explanation of how to interact with the plot and the mathematics behind it.

## Obtaining the Roots
The roots and multiplicities displayed in the two plots are read from the
file **data/roots.txt**. This file has been generated with the Python
packag Froots, which is available at https://github.com/hmalcha/Froots. 
Froots is based on the SimpLie program written by Teake Nutma 
(https://github.com/teake/simplie). However, compared to SimpLie
Froots allows for the calculation of roots with arbitrary height by
implementing custom classes for large integers and fractions.


## License
Copyright © 2024 Hannes Malcha

VisualLie is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

VisualLie is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VisualLie. If not, see https://www.gnu.org/licenses/.
