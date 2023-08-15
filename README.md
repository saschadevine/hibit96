# hibit96

## Description
Script for normalizing test-well RLU data to on-plate vehicle-well RLU data, as acquired by a GloMax Discover. With such data, this script will:

- Collect all data (and all its annotations: treatments & doses)

- From all data, collect vehicle-well data

- Re-express all data as percent of vehicle-well-in-column

- Output raw and normalized data, well by well, with annotations

This script was designed around 96wp CCNE1 HiBiT assay output, but could normalize any 96wp RLU data acquired on a GloMax Discover (e.g., would be acceptable for normalizing CellTiter-Glo data, given same plate layout)

## Input Requirements
- ```data.csv```: CSV output from GloMax Discover
- ```annot.csv```: List of treatment annotations
- ```doses.csv```: List of doses, in uM (expect 3 doses)
