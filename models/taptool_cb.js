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
 * This is the callback function for the taptool.
 * It draws the Weyl orbits, which is a parabola
 * and highlights the roots in the Weyl orbit.
 * 
 * There are two variations of this function depending
 * on the choice of Weyl orbit. Either the full orbit is
 * shown or only the translation group orbit.
 */


//
// First part: Definitions to compute Weyl orbits
//

// Define the simple roots and the simple co-roots
const SIMPLEROOTS = [[0, 1, 0], [0, 0, 1]];
const SIMPLECOROOTS = [[-1, 2, -2], [0, -2, 2]];

/**
 * Compute the Weyl reflection of a root with respect to
 * the i'th simple root.
 * @param {Root} root 
 * @param {Int} i 
 * @returns The reflected root
 */
function weyl_reflection(root, i) {
    const dotProduct = root.reduce((sum, val, index) => sum + val * SIMPLECOROOTS[i][index], 0);
    return root.map((val, index) => val - SIMPLEROOTS[i][index] * dotProduct);
}

/**
 * Get the depth of a root.
 * @param {Root} root 
 * @returns The depth of the root
 */
function depth(root) {
    return root[1];
}

/**
 * Check if a root is already in the given Weyl orbit.
 * @param {Root} root 
 * @param {Array.<Root>} orbit 
 * @returns true or false
 */
function is_in_orbit(root, orbit) {
    if (orbit.length === 1) {
        return JSON.stringify(root) === JSON.stringify(orbit);
    } else {
        return orbit.some(elem => JSON.stringify(elem) === JSON.stringify(root));
    }
}


/**
 * Find all roots in the Weyl orbit of a given root up to a given maximal 
 * depth and for two given reflections.
 * @param {Array.<Root>} roots 
 * @param {Array.<Root>} orbit 
 * @param {Int} max_depth 
 * @param {Function} reflection_1 
 * @param {Function} reflection_2 
 * @returns The Weyl orbit
 */
function find_orbit(roots, orbit, max_depth, reflection_1, reflection_2) {
    let new_roots = [];
    let new_orbit = orbit.slice();

    for (const root of roots) {
            const new_root_1 = reflection_1(root);
            const new_root_2 = reflection_2(root);

            if (!is_in_orbit(new_root_1, new_orbit) && depth(new_root_1) <= max_depth) {
                new_orbit.push(new_root_1);
                new_roots.push(new_root_1);
            }

            if (!is_in_orbit(new_root_2, new_orbit) && depth(new_root_2) <= max_depth) {
                new_orbit.push(new_root_2);
                new_roots.push(new_root_2);
            }
        }

    if (new_roots.length === 0) {
        return new_orbit.sort((a, b) => {for (let i = 0; i < a.length; i++) {
            if (a[i] !== b[i]) {
                return a[i] - b[i];
            }
        }
        return 0;
    });
    } else {
        return find_orbit(new_roots, new_orbit, max_depth, reflection_1, reflection_2);
        
    }
}


/**
 * Compute the full Weyl orbit of a root up to a given depth
 * @param {Root} root 
 * @param {Int} maxDepth 
 * @returns The Weyl orbit
 */
function weyl_orbit_computer(root, maxDepth) {
    function reflection_1(root){
        return weyl_reflection(root,0);
    }
    function reflection_2(root){
        return weyl_reflection(root,1);
    }
    return find_orbit([root], [root], maxDepth, reflection_1, reflection_2)
}


/**
 * Compute the translation group orbit of a given root up to the given depth.
 * @param {Root} root 
 * @param {Int} maxDepth 
 * @returns The translation group orbit.
 */
function translation_orbit_computer(root, maxDepth) {
    function reflection_1(root){
        return weyl_reflection(weyl_reflection(root,0),1);
    }
    function reflection_2(root){
        return weyl_reflection(weyl_reflection(root,1),0);
    }
    return find_orbit([root], [root], maxDepth, reflection_1, reflection_2)
}


//
// First part: The callback function
//

// Compute the orbit depending on the radio button setting.
// Highlight the roots in the orbit and draw the parabola 
// through the highlighted roots.
for (let i = 0; i < MAXLEVEL; i++){
    if (root_plots[i].visible){
        const selected_index = sources_roots[i].selected.indices;
        if (selected_index){
            const level = i + 1;
            let orbit;
            if (radio_button_group.active == 0){
                orbit = weyl_orbit_computer([level, sources_roots[i].data['r0'][selected_index[0]], sources_roots[i].data['r1'][selected_index[0]]], MAXDEPTH);
            }
            else{
                orbit = translation_orbit_computer([level, sources_roots[i].data['r0'][selected_index[0]], sources_roots[i].data['r1'][selected_index[0]]], MAXDEPTH);
            }
                
            const xVal = orbit.map(root => root[2] - root[1]);
            const yVal = orbit.map(root => - root[1]);

            const xMax = Math.sqrt(-level * orbit[0][1] + Math.pow(orbit[0][1] - orbit[0][2], 2) + 30 * level);

            const parabola_x = Array.from({ length: 100 }, (_, i) => -xMax + (i * (2 * xMax) / 99));
            const parabola_y = parabola_x.map(val => -1 / level * Math.pow(val, 2) - orbit[0][1] + Math.pow(orbit[0][1] - orbit[0][2], 2) / level);
                           
            source_parabola.data = {parabola_x, parabola_y};
            parabola.visible = true;
                
            source_Weyl_Orbit.data = {xVal, yVal};
            wo_plot.visible = true;
        }
        else{
            wo_plot.visible = false;
            parabola.visible = false;
        }
    }
}