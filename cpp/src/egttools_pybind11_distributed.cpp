/** Copyright (c) 2022-2023  Elias Fernandez
*
* This file is part of EGTtools.
*
* EGTtools is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* EGTtools is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with EGTtools.  If not, see <http://www.gnu.org/licenses/>
*/

#include <pybind11/pybind11.h>

#include "version.h"

#define XSTR(s) STR(s)
#define STR(s) #s

namespace py = pybind11;
using namespace std::string_literals;

void init_methods(py::module_ &);
void init_games(py::module_ &);
void init_behaviors(py::module_ &);
void init_datastructures(py::module_ &);
void init_distributions(py::module_ &);

PYBIND11_MODULE(numerical, m) {
    m.attr("__version__") = py::str(XSTR(EGTTOOLS_VERSION));
    m.attr("VERSION") = py::str(XSTR(EGTTOOLS_VERSION));
    m.attr("__init__") = py::str(
            "The `numerical` module contains optimized "
            "functions and classes to simulate evolutionary dynamics in large populations.");

    m.doc() =
            "The `numerical` module contains optimized functions and classes to simulate "
            "evolutionary dynamics in large populations. This module is written in C++.";

    // Now we define a submodule
    auto mGames = m.def_submodule("games");
    auto mBehaviors = m.def_submodule("behaviors");
    auto mData = m.def_submodule("DataStructures");
    auto mDistributions = m.def_submodule("distributions");

    mGames.attr("__init__") = py::str("The `egttools.numerical.games` submodule contains the available games.");
    mBehaviors.attr("__init__") = py::str("The `egttools.numerical.behaviors` submodule contains the available strategies to evolve.");
    mData.attr("__init__") = py::str("The `egttools.numerical.DataStructures` submodule contains helpful data structures.");
    mDistributions.attr("__init__") = py::str(
            "The `egttools.numerical.distributions` submodule contains "
            "functions and classes that produce stochastic distributions.");

    init_methods(m);
    init_games(mGames);
    init_behaviors(mBehaviors);
    init_datastructures(mData);
    init_distributions(mDistributions);
}