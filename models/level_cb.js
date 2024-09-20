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
 * This is the callback function for the level selector.
 * The function resets all additional plot features
 * and makes the roots of the newly selected level visible.
 * Also the title is changed to show the current level.
 */


for (let i = 0; i < max_level; i++){
    root_plots[i].visible = false
    labels[i].visible = false
    ref_lines_2[i].visible = false
    ref_lines_labels[i].visible = false
}
wo_plot.visible = false
parabola.visible = false
plot.title.text = "Roots of F on Level " + ticker.value
root_plots[ticker.value-1].visible = true