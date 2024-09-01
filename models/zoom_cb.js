// This file is part of VisualLie.
//
// Copyright (C) 2024 Hannes Malcha 
//
// VisualLie is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// VisualLie is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with VisualLie.  If not, see <https://www.gnu.org/licenses/>.

/**
 * VisualLie is a web app to visualize the root system of the
 * Feingold-Frenkel algebra.
 *
 * This is the callback function for the zoom setting.
 * It changes the font size of the root multiplicity when the user
 * zooms in or out of the root lattice plot.
 */

var xr = [plot.x_range.start,plot.x_range.end]
                   for (let i = 0; i < MAXLEVEL; i++){
                        if (root_plots[i].visible && checkboxes.active.includes(0) && xr[1]-xr[0] < 15){
                            labels[i].text_font_size="15px"
                            } else {
                            labels[i].text_font_size="10px"
                            }
                        }