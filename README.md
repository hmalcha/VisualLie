# VisualLie

VisualLie is a web app that visualizes the root system of the Feingold-Frenkel
algebra. It uses the Bokeh Python library to generate an interactive plot of
the root system. The plot is embedded in a web page providing detailed
explanations of all its properties.

The VisualLie web app is available at

https://hmalcha.github.io/VisualLie/

For a local version of VisualLie, download the
**VisualLie.html** file and open with your favorite web browser.

## Getting Started
If you want to modify VisualLie or build the **VisualLie.html** file yourself,
follow these steps. 

VisualLie requires a Python installation with 
[Bokeh](https://docs.bokeh.org/en/latest/index.html).
To install Bokeh using `pip`, enter

```
pip install bokeh
```

Then you can run **VisualLie.py** to build **VisualLie.html** using

```
python VisualLie.py
```

## Usage
VisualLie is self-contained. When you visit
https://hmalcha.github.io/VisualLie/
or open the **VisualLie.html** file you are presented with a detailed
explanation of how to interact with the plot and the mathematics behind it.

To learn more about the Bokeh plot tools, visit the
[Bokeh documentation](https://docs.bokeh.org/en/latest/docs/user_guide/interaction/tools.html).

## Rootsystem
Included in VisualLie is a Python package called **rootsystem**. It constructs
the root system of the Feingold-Frenkel algebra. This package is based on the
SimpLie program written by Teake Nutma, which is available at
https://github.com/teake/simplie.

**rootsystem** requires a Python installation with [NumPy](https://numpy.org/).
To install NumPy using `pip`, enter

```
pip install numpy
```

**rootsystem** is called with one optional argument from the command line.
The argument is the height up to which the root system will be constructed.
If no argument is given, the calculation defaults to a height of 76.

Upon executing the **rootsystem** package, the root system is automatically
constructed up to the given height and stored as a CSV file in the data/ 
folder. The first three numbers in each row are the root vector and
the last number is the multiplicity of that root.

To run the package type

```
python -m rootsystem [HEIGHT]
```
where [HEIGHT] is the optional argument. It can be either nothing or a 
positive integer.

Note that the root multiplicities are huge numbers. When constructing the
root system of the Feingold-Frenkel algebra for heights > 80, there are
some issues due to dealing with numbers greater than 2^64. This will
hopefully be fixed in a future version.

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
