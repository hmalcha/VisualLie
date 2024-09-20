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
 * This is the callback function for the checkboxes.
 * It changes the visibility of the various plot features
 * according to the selected checkboxes.
 */

for (let i = 0; i < max_level; i++){
    if (root_plots[i].visible){
        var xr = [plot.x_range.start,plot.x_range.end]
        labels[i].visible = checkboxes.active.includes(0)
        arrow_labels.visible = checkboxes.active.includes(1)
        arrow_0.visible = checkboxes.active.includes(1)
        arrow_1.visible = checkboxes.active.includes(1)
        ref_line_1.visible = checkboxes.active.includes(1)
        ref_lines_2[i].visible = checkboxes.active.includes(1)
        ref_lines_labels[i].visible = checkboxes.active.includes(1)
        }
    }