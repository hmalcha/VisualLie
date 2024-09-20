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
 * This callback function is called when the level changes.
 * It hides the Weyl orbits and resets the taptool.
 */

// Hide the Weyl orbit and the parabola.
wo_plot.visible = false
parabola.visible = false
// Reset the selected root.
for (let i = 0; i < max_level; i++){
    sources_roots[i].selected.indices = [];
    sources_roots[i].change.emit();
}