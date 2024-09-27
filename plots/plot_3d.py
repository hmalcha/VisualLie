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
import math
import plotly.express as px
import plotly.graph_objs as go

def make_3d_plot(max_depth, max_level):

    #########################
    #                       #
    # Prepare the plot data #
    #                       #
    #########################

    # Generate elements of the root lattice [x, y, z] as matrices with entries
    # [[x-y, z-y], [z-y, -x]]  
    root_matrices = [np.array([[a,b],[b,-level]]) for level in range(1,max_level)
                                                for a in range(-max_depth, max_depth)
                                                for b in range(-max_depth, max_depth)]
    
    # The root system consists of those matrices with det() >= -1
    # Write the elements of the root system into tuples for plotting
    level, root_x, root_y, root_z = zip(*[
        (
            "Level " + str(-m[1][1]),
            1/2*(m[0][0] - m[1][1]),
            m[0][1],
            1/2*(m[0][0] + m[1][1])
        )
        for m in root_matrices
        if np.linalg.det(m) >= -1 and -1/2*(m[0][0] + m[1][1]) < math.floor(max_depth/2) +1
    ])
    
    # Convert the tuples to list
    level, root_x, root_y, root_z = map(list, [level, root_x, root_y, root_z])

    # A a little bit of whitespace to the the first three plot labels
    # This improves the behavior of the plot labels together with the
    # buttons
    for i in range(len(level)):
        if level[i] == "Level 1" or level[i] == "Level 2" or level[i] == "Level 3":
            level[i] = level[i] + "  "

    # Create a pandas data frame from the lists 
    df_roots = pd.DataFrame(data={
        'level': level,
        'x': root_x,
        'y': root_y,
        'z': root_z})
    
    # Define a hyperboloid with radius 1
    u_vals = np.linspace(-2.84, 1)
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
    
    # Define a color sequence for the roots
    color_sequence = [
        '#000080',  # Navy
        '#008000',  # Green
        '#FF4500',  # Orange Red
        '#008B8B',  # Dark Teal
        '#9932CC',  # Dark Orchid
        '#FF8C00',  # Dark Orange
        '#4169E1',  # Royal Blue
        '#50C878',  # Emerald Green
        '#8B4513',  # Saddle Brown
        '#000000',  # Black
        '#9B111E',  # Ruby Red
        '#808000',  # Olive
        '#DDA0DD',  # Plum
        '#B8860B',  # Dark Goldenrod
        '#36454F',  # Charcoal
        '#C71585',  # Medium Violet Red
        '#4682B4'   # Steel Blue
    ]
    
    # Create a 3D scatter plots from the roots
    fig = px.scatter_3d(df_roots, x='x', y='y', z='z',
                        color='level',
                        color_discrete_sequence=color_sequence,
                        opacity=1,
                        hover_data=None
                        )
    
     # Set the visibility to True
    fig.update_traces(visible=True, selector=dict(type='scatter3d'))
    
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
            text="Roots of F on Levels 1 to 17",
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
    # Set the initial camera position
    fig.update_layout(scene_camera=dict(eye=dict(x=-1.6, y=1.4, z=1)))
    
    # Define the plot legend
    fig.update_layout(legend=dict(title="",
                                  font=dict(size=16,
                                            family="Helvetica",
                                            color='black'),
                                  xanchor="left",
                                  x=1,
                                  y=0.4))
  
    #############################
    #                           #
    # Make the user interaction #
    #                           #
    #############################    
    
    # Add a button to show / hide the hyperboloid
    fig.update_layout(updatemenus=[
    dict(type="buttons",
         direction="down",
         pad={"r": -100, "t": 20},
         showactive=True,
         x=1,
         xanchor="right",
         y=.8,
         yanchor="middle",
         buttons=list([
            dict(label="Reset",
                 method="update",
                 args=[{"visible":[True] * (max_level - 2) + [False]},
                       {'title': "Roots of F on Levels 1 to 17"}]),
            dict(label="Hyperboloid",
                 method="update",
                 args=[{"visible": [True] * (max_level - 2) + [True]},
                       {'title': "Roots of F on Levels 1 to 17"}]),
            dict(label="Levels 1 - 3",
                 method="update",
                 args=[{"visible": [True] * 3 + [False] * (max_level -3)},
                       {'title': "Roots of F on Levels 1 to 3"}])
                ])
        )
    ])
    
    # Add a title for the buttons
    fig.update_layout(annotations=[
            dict(text="Modify Plot:",
                 x=1.145,
                 y=.9,
                 align="left",
                 showarrow=False,
                 font=dict(size=16,
                           color="black",
                           family="Helvetica",
                           weight="bold"))
            ])
    
    
    ######################################
    #                                    #
    # Return a html document of the plot #
    #                                    #
    ######################################
    
    return(fig.to_html(full_html=False))