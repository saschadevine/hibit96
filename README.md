# hibit96

## Description
Script for normalizing test-well RLU data to on-plate vehicle-well RLU data, as acquired as comma-separated values (CSV) by a GloMax Discover instrument.

With such data, this script will:

- Collect all data (and all its annotations: treatments & doses)

- From all data, collect vehicle-well data

- Re-express all data as percent of vehicle-well-in-column

- Output raw and normalized data, well by well, with annotations

This script was designed around 96wp CCNE1 HiBiT assay output, but could normalize any 96wp RLU data acquired on a GloMax Discover instrument (e.g., would be acceptable for normalizing CellTiter-Glo data, given same plate layout)

## Input Requirements
- ```data.csv```: CSV output from GloMax Discover
- ```annot.csv```: List of treatment annotations
- ```doses.csv```: List of doses, in uM (expect 3 doses)

## License Information
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
