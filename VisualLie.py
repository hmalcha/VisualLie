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

This python module uses the Bokeh Python library to generate an interactive
plot of the root system of the Feingold-Frenkel algebra. The plot is
supplemented with a documentation stored in the templates/ folder and saved
as VisualLie.html. This .html file can be viewed with any modern web browser.

The interactivity of the plot is realized through JS callback functions.
These are stored in the the models/ folder. The data for the plots is imported
from the models/ folder.


For more information on Bokeh see:

Bokeh Development Team (2018). Bokeh: Python library for interactive visualization
URL http://www.bokeh.pydata.org.
"""

import numpy as np
from bokeh.models import Arrow, NormalHead, Range1d
from bokeh.models import ColumnDataSource, LabelSet, CustomJS, Select, Div
from bokeh.models import CheckboxGroup, HoverTool, TapTool, RadioButtonGroup
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN
from jinja2 import Environment, FileSystemLoader


##################################
#                                #
# Set parameters and import data #
#                                #
##################################

# Define the maximum depth and level for the plots
MAXDEPTH = 30
MAXLEVEL = 5


def norm(root):
    """Compute the norm of a root from its root vector"""
    return np.dot(root, np.dot(root, np.array([[2,-1,0],[-1,2,-2],[0,-2,2]])))


# Import the roots from the models/ folder
try:
    roots = np.genfromtxt('data/roots.txt', delimiter=',',dtype=int)
except IOError:
    print("Could not find roots.txt in models/.") 

# Each row in roots is a list with the four entires
# [level, depth, spin label, multiplicity]


# We sort the roots of level 1 to MAXLEVEL into a new list:
roots_sorted = [[[] for _ in range(4)] for _ in range(MAXLEVEL)]       
for elem in roots:
    if elem[0] > 0 and elem[0] <= MAXLEVEL and elem[1] <= MAXDEPTH:
        roots_sorted[elem[0] - 1][0].append(np.int64(elem[1]).item())
        roots_sorted[elem[0] - 1][1].append(np.int64(elem[2]).item())
        roots_sorted[elem[0] - 1][2].append(np.int64(elem[3]).item())
        roots_sorted[elem[0] - 1][3].append(np.int64(norm(elem[:3])).item())


###################
#                 #
# Create the plot #
#                 #
###################

# Create a new bokeh plot
plot = figure(x_axis_label="Weight", y_axis_label="Depth")

# Make the wheel zoom active
#plot.toolbar.active_scroll = plot.toolbar.tools[1]

# Customize the grid lines
#plot.xaxis.visible = False
#plot.yaxis.visible = False
plot.xgrid.visible = False
#plot.ygrid.visible = False

# Set the plot dimensions and the plot range
plot.frame_width = 650
plot.frame_height = 650
plot.x_range = Range1d(-12, 12)
plot.y_range = Range1d(-31, 3)

# Set the plot title
plot.title.text = "Roots of F on Level 1"
plot.title.align = "center"
plot.title.text_font_size = "25px"


########################
#                      #
# Add data to the plot #
#                      #
########################

# Define the list of sources for plotting the roots
# label, level, r0 and r1 are used to display data with the hover tool defined below
sources_roots = []

for i in range(MAXLEVEL):
    sources_roots.append(ColumnDataSource(data=dict(
        xVal = [x - y for x, y in zip(roots_sorted[i][1], roots_sorted[i][0])],
        yVal = list(map(lambda x: (-1)*x, roots_sorted[i][0])),
        mult = roots_sorted[i][2],
        level = [i+1] * len(roots_sorted[i][0]),
        r0 = roots_sorted[i][0],
        r1 = roots_sorted[i][1],
        norm = roots_sorted[i][3]
        )))

   
# Define the list of sources for plotting the labels
sources_labels = []

for i in range(MAXLEVEL):
    sources_labels.append(ColumnDataSource(data=dict(
        xVal = [x - y + 3/16 for x, y in zip(roots_sorted[i][1], roots_sorted[i][0])],
        yVal = list(map(lambda x: (-1)*x - 3/8, roots_sorted[i][0])),
        mult = roots_sorted[i][2]
        )))


# Define the source for the Weyl orbits
source_Weyl_Orbit = ColumnDataSource(data=dict(xVal = [], yVal = []))

# Define the source for the parabola
parabola_x = np.arange(-5.5, 5.6, 0.1)
parabola_y = -np.square(parabola_x)
source_parabola = ColumnDataSource(data=dict(parabola_x=parabola_x, parabola_y=parabola_y))


# Plot the roots and show only the level 1 roots
root_plots = []

for i in range(MAXLEVEL):
    root_plots.append(plot.circle('xVal', 'yVal', source=sources_roots[i], color="navy", radius=.1))
    if i > 0:
        root_plots[i].visible = False


# Plot the Weyl-Orbit and hide it
wo_plot = plot.circle('xVal', 'yVal', source=source_Weyl_Orbit, color="green", radius=.1)
wo_plot.visible = False


# Plot the labels and hide them all
labels = []
for i in range(MAXLEVEL):
    labels.append(LabelSet(x='xVal',y='yVal', text='mult', source=sources_labels[i], background_fill_color = "white", text_font_size="10px"))
    labels[i].visible = False
    plot.add_layout(labels[i])


# Plot a parabola and hide it
parabola = plot.line('parabola_x','parabola_y',source=source_parabola, line_width=2, line_alpha=.5, color="green")
parabola.visible = False


# Plot the simple root arrows and hide them
source_arrow_label = ColumnDataSource(data=dict(x=[-7,-5], y=[0,-1], label=['a_0', 'a_1']))
arrow_labels = LabelSet(x='x', y='y', text='label', source=source_arrow_label, x_offset=5, y_offset=5)
arrow_0 = Arrow(end=NormalHead(size=10, fill_color="orange", line_color="orange"), x_start=-6, y_start=-1, x_end=-7, y_end=0, line_color="orange")
arrow_1 = Arrow(end=NormalHead(size=10, fill_color="orange", line_color="orange"), x_start=-6, y_start=-1, x_end=-5, y_end=-1, line_color="orange")

arrow_0.visible = False
arrow_1.visible = False
arrow_labels.visible = False
plot.add_layout(arrow_0)
plot.add_layout(arrow_1)
plot.add_layout(arrow_labels)


# Plot the reflection lines and hide them
ref_line_1 = plot.line([0,0], [0,-30], line_width=2, color="orange")
ref_line_1.visible = False
ref_lines_2 = []
source_ref_lines_label = []
ref_lines_labels = []
for i in range(MAXLEVEL):
    ref_lines_2.append(plot.line([(i+1)/2,(i+1)/2], [0,-30], line_width=2, color="orange"))
    ref_lines_2[i].visible = False
    source_ref_lines_label.append(ColumnDataSource(data=dict(x=[0,(i+1)/2], y=[0,0], label=['r_1', 'r_0'], x_offset=[-20,0])))
    ref_lines_labels.append(LabelSet(x='x', y='y', text='label', x_offset='x_offset', y_offset=10, source=source_ref_lines_label[i], background_fill_color = "white"))
    ref_lines_labels[i].visible = False
    plot.add_layout(ref_lines_labels[i])


##############################
#                            #
# Make the user interactions #
#                            #
##############################


# Make the hover tool, add it to the plot and make it active only in the roots
TOOLTIPS = [("Root", "[@level, @r0, @r1]"), ("Norm", "@norm"), ("Multiplicity", "@mult")]
hovertool = HoverTool(tooltips=TOOLTIPS)
plot.add_tools(hovertool)
hovertool.renderers = [p for p in root_plots]


# Make the tap tool, add it to the plot and make it active only in the roots
taptool = TapTool()
plot.add_tools(taptool)
taptool.renderers = [p for p in root_plots]


# Add a selector for the level
OPTIONS = [str(i) for i in range(1, MAXLEVEL + 1)]
ticker = Select(value="1", options=OPTIONS, title="Select the level:", styles={'font-size': '14px'}, width = 100)


# Add checkboxes for showing the multiplicities and Weyl reflections
CHECKBOX_LABELS = ["Multiplicities", "Weyl Reflections"]
checkboxes = CheckboxGroup(labels=CHECKBOX_LABELS, active=[], styles={'font-size': '14px'})


# Add radio buttons for the type of Weyl orbit
BUTTON_LABELS = ["Full", "Translation"]
radio_button_group = RadioButtonGroup(labels=BUTTON_LABELS, active=0, styles={'font-size': '14px'})


#########################
#                       #
# JS callback functions #
#                       #
#########################

# Define the JS callback functions for the user interactions.
# The JS code is saved in the models/ folder


# Callback for changing the font size of the multiplicities depending on the zoom
zoom_cb = CustomJS(args=dict(labels=labels, plot=plot, checkboxes=checkboxes, root_plots=root_plots, MAXLEVEL=MAXLEVEL),
                    code=open("models/zoom_cb.js").read()
                    )


# Callback function for the checkboxes
checkbox_cb =  CustomJS(args=dict(labels=labels, plot=plot, checkboxes=checkboxes, arrow_0=arrow_0, arrow_1=arrow_1, arrow_labels=arrow_labels, 
                                  ref_line_1=ref_line_1, ref_lines_2=ref_lines_2, ref_lines_labels=ref_lines_labels,
                                  root_plots=root_plots, MAXLEVEL=MAXLEVEL),
                    code=open("models/checkbox_cb.js").read()
                    )


# Callback function for the level selector
level_cb = CustomJS(args=dict(ticker=ticker, labels=labels, plot=plot, root_plots=root_plots, wo_plot=wo_plot, 
                              ref_lines_2=ref_lines_2, ref_lines_labels=ref_lines_labels, parabola=parabola, MAXLEVEL=MAXLEVEL),
                    code=open("models/level_cb.js").read()
                    )


# This is the callback function for the taptool
taptool_cb = CustomJS(args=dict(root_plots=root_plots, sources_roots=sources_roots, parabola=parabola, source_parabola=source_parabola,
                                wo_plot=wo_plot, source_Weyl_Orbit=source_Weyl_Orbit, radio_button_group=radio_button_group, MAXLEVEL=MAXLEVEL, MAXDEPTH=MAXDEPTH),
                      code=open("models/taptool_cb.js").read())


# Callback function for resetting the taptool
reset_taptool_cb = CustomJS(args=dict(parabola=parabola, wo_plot=wo_plot, sources_roots=sources_roots, MAXLEVEL=MAXLEVEL),
                      code=open("models/reset_taptool_cb.js").read())


# Define which user interaction triggers which callback function
plot.x_range.js_on_change('end', zoom_cb)
checkboxes.js_on_change("active", checkbox_cb, zoom_cb)
ticker.js_on_change('value', level_cb, checkbox_cb, reset_taptool_cb, zoom_cb)
plot.js_on_event('tap', taptool_cb)
radio_button_group.js_on_event("button_click", reset_taptool_cb)


##################
#                #
# Style the plot #
#                #
##################

# Write the description displayed next to the plot
description_1 = Div(text="""<p>Use the level selector, checkboxes, and buttons to
                    interact with the plot.</p>""", styles={'text-align': 'justify', 'font-size': '14px'}, width=180)
description_2 = Div(text="""Note: At higher levels and depths, the multiplicities 
                    become quite large, so it is advised to use the bokeh plot 
                    tools on the right to zoom into the root system.""", styles={'text-align': 'justify', 'font-size': '14px'}, width=180)
 
# Make a heading for the checkboxes and radio buttons
checkbox_heading = Div(text="""<p>Show or hide additional plot elements:</p>""", styles={'font-size': '14px'}, width=180)
radio_button_heading = Div(text="""<p>Select the type of Weyl orbit:</p>""", styles={'font-size': '14px'}, width=180)

# Define padding boxes
v_padding_1 = Div(width=180, height=25)
v_padding_2 = Div(width=180, height=20)
v_padding_3 = Div(width=180, height=20)
v_padding_4 = Div(width=180, height=20)
v_padding_5 = Div(width=180, height=25)

# Put all the widgets and text elements together
widgets = column(v_padding_1, description_1, v_padding_2, ticker,
                v_padding_3, checkbox_heading, checkboxes, 
                v_padding_4, description_2,
                v_padding_5, radio_button_heading, radio_button_group, width=200)


#######################################
#                                     #
# Embed the plot in the html template #
#                                     #
#######################################

# Create an html document that embeds the bokeh plot
html_plot = file_html(row(widgets, plot), CDN, "VisualLie_Plot")

# Load the html environment
environment = Environment(loader=FileSystemLoader("templates"))

# Specify the template
template = environment.get_template("main_template.html.jinja")

# Insert the plot and the text into the template
rendered_template = template.render(html_plot=html_plot)

# Save the plot embedded into the html template to a file
try:
    with open("VisualLie.html", "w") as f:
        f.write(rendered_template)
except IOError:
    print("Could not write the file.") 
    
# Save the html file to the docs/ folder for integration with GitHub Pages
try:
    with open("docs/index.html", "w") as f:
        f.write(rendered_template)
except IOError:
    print("Could not write the file.") 