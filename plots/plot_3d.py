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

This python module creates the 3D plot and returns it as an html document.

The 3D plot is created using the Python library Plotly. For more information
on Plotly see:

Plotly Technologies Inc. Collaborative data science. Montréal, QC, 2015. 
https://plot.ly.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def make_3d_plot():

    #########################
    #                       #
    # Prepare the plot data #
    #                       #
    #########################

    # Import the roots from the data/ folder
    try:
        roots = np.genfromtxt('data/roots.txt', delimiter=',',dtype=int)
    except IOError:
        print("Could not find roots.txt in data/.") 

    # Keep only the roots of level 1 to 3 and up to height 14
    level, root_x, root_y, root_z = zip(*[
        (
            np.int64(elem[0]).item(),
            np.int64(elem[1]-elem[2]).item(),
            np.int64(-1+elem[0]-elem[1]).item(),
            np.int64(-elem[0]-elem[1]).item()
        )
        for elem in roots
        if 0 < elem[0] < 4 and elem[1] < 15
    ])

    # Convert the tuples to list
    level, root_x, root_y, root_z = map(list, [level, root_x, root_y, root_z])

    # Turn the list of levels into a list of strings for the plot legend
    level = ["Level " + str(i) for i in level]

    # Create a pandas data frame from the data 
    df_roots = pd.DataFrame(data={
        'level': level,
        'x': root_x,
        'y': root_y,
        'z': root_z})
    
    # Define a hyperboloid
    u_vals = np.linspace(-3.5, 2)
    v_vals = np.linspace(0,2*np.pi)
    u, v = np.meshgrid(u_vals, v_vals)
    
    hyperboloid_x = np.cosh(u) * np.cos(v)
    hyperboloid_y = np.cosh(u) * np.sin(v)
    hyperboloid_z = np.sinh(u)
    
    
    ###################
    #                 #
    # Create the plot #
    #                 #
    ###################
    
    
    # Create a 3D scatter plots from the roots
    fig = px.scatter_3d(df_roots, x='x', y='y', z='z',
                        color='level',
                        color_discrete_sequence=["navy", "green", "red"],
                        opacity=1,
                        hover_data=None
                        )
    
    # Set the marker size
    fig.update_traces(marker_size=9)
    
    # Add the hyperboloid to the plot and hide it
    fig.add_trace(go.Surface(x = hyperboloid_x,
                             y = hyperboloid_y,
                             z = hyperboloid_z,
                            surfacecolor=np.full(hyperboloid_z.shape, fill_value=1),
                            colorscale=[[0, 'darkorange'], [1, 'darkorange']],
                            showscale=False,
                            opacity=0.5,
                            visible=False,       
                            ))

    ##################
    #                #
    # Style the plot #
    #                #
    ##################

    # Add a title
    # Add and customize the title
    fig.update_layout(
        title=dict(
            text="Roots of F on Levels 1 to 3",
            x=0.5,
            y=0.95,
            xanchor="center",
            yanchor="top",
            font=dict(
                size=25,
                color="black",
                family="Helvetica",
                weight="bold"
            ))
        )

    # Set the general plot dimensions
    fig.update_layout(width=800, height=800, autosize=False,
                      margin=dict(t=20, b=0, l=0, r=0)
                      )

    # Hide all the hover info
    fig.update_traces(hoverinfo='none',
                      hovertemplate=None)
    
    # Style the axes
    axis_style = dict(showspikes=False,
                      showticklabels=False,
                      backgroundcolor='rgba(0, 0, 0, 0)',
                      title = "")

    fig.update_layout(scene=dict(xaxis=axis_style,
                                 yaxis=axis_style,
                                 zaxis=axis_style
                                ))
    # Set the camera position
    fig.update_layout(scene_camera=dict(eye=dict(x=-1.5, y=-1.5, z=0.8)))
    
    # Define the plot legend
    fig.update_layout(legend=dict(title="",
                                  font=dict(size=16, color='black'),
                                  x=1,
                                  y=0.5))
  
    #############################
    #                           #
    # Make the user interaction #
    #                           #
    #############################    
  
    
    # Add a button to show / hide the hyperboloid
    fig.update_layout(updatemenus=[
            dict(type="buttons",
                 direction="right",
                 pad={"l": 10, "t": 20},
                 showactive=True,
                 x=1,
                 xanchor="left",
                 y=.90,
                 yanchor="middle",
                 buttons=list([
                    dict(label="Off",
                         method="update",
                         args=[{"visible": [True, True, True, False]}]),
                    dict(label="On",
                         method="update",
                         args=[{"visible": [True, True, True, True]}])
                    ])
            )])

    # Add a title for the buttons
    fig.update_layout(annotations=[
            dict(text="Hyperboloid:",
                 x=1,
                 y=.90,
                 align="left",
                 showarrow=False,
                 font=dict(size=16, color='black'),
                 opacity=1)
            ])
    
    
    ######################################
    #                                    #
    # Return a html document of the plot #
    #                                    #
    ######################################
    
    return(fig.to_html(full_html=False))