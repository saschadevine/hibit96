# hibit96

Script for normalizing test-well RLU data to on-plate vehicle-well RLU data, as acquired by a GloMax Discover
- Given RLU data acquired as CSV from a 96w HiBiT assay plate, this script will:
      - Collect all data (and all its annotations: treatments & doses)
      - From all data, collect vehicle-well data
      - Re-express all data as percent of vehicle-well-in-column
      - Output raw and normalized data, well by well, with annotations
- Script was designed around 96wp CCNE1 HiBiT assay output, but could normalize any 96wp RLU data acquired on a GloMax Discover:
      - E.g., would be acceptable for normalizing CellTiter-Glo data, given same plate layout
