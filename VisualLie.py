#!/usr/bin/env python3

# This file is part of VisualLie.
#
# Copyright (C) 2024 Hannes Malcha 
#
# VisualLie is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# VisualLie is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with VisualLie.  If not, see <https://www.gnu.org/licenses/>.
#
#
# This class is an exact copy of the Root class from the SimpLie programm
# written by Teake Nutma, which is available at
# https://github.com/teake/simplie.

"""
VisualLie is a web app to visualize the root system of the Feingold-Frenkel
algebra.

This python module uses the jinja2 library to assemble all the different files
into one .html file.

First the 2D and 3D plots are created by calling the make_2d_plot and
make_3d_plot functions from the plot_2d.py and plot_3d.py files in 
the plots/ directory. 

Then the plots and all the .html.jinja files from the templates/ directory
are integrated into the main_template.html.jinja and one html document
is rendered.

The document is saved as VisuaLie.html in notebook directory and
and as index.html in the docs/ directory.
"""

from jinja2 import Environment, FileSystemLoader
from plots.plot_2d import make_2d_plot
from plots.plot_3d import make_3d_plot

# Define the maximum depth and level for the 2D plots
MAXDEPTH = 30
MAXLEVEL = 5

# Create the 2D Plot
html_2d_plot = make_2d_plot(MAXDEPTH, MAXLEVEL)
html_3d_plot = make_3d_plot()

# Load the html environment
environment = Environment(loader=FileSystemLoader("templates"))

# Specify the template
template = environment.get_template("main_template.html.jinja")

# Insert the plot and the text into the template
rendered_template = template.render(html_2d_plot=html_2d_plot, html_3d_plot=html_3d_plot)

# Save the plot embedded into the html template to a file
# This is disabled for GitHub
"""
try:
    with open("VisualLie.html", "w") as f:
        f.write(rendered_template)
except IOError:
    print("Could not write the file.") 
"""
    
# Save the html file to the docs/ folder for integration with GitHub Pages
try:
    with open("docs/index.html", "w") as f:
        f.write(rendered_template)
except IOError:
    print("Could not write the file.") 