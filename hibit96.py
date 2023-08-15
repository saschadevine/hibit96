#!/usr/bin/python3
#



#
# hibit96: hibit96.py
# (C) SLD 2023
#
#
#
# LICENSE
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see https://www.gnu.org/licenses/.
#
#
#
# DESCRIPTION
#
# Script for normalizing test-well RLU data to on-plate vehicle-well RLU data,
# as acquired by a GloMax Discover
# - Given RLU data acquired as CSV from a 96w HiBiT assay plate, this script
#   will:
#       - Collect all data (and all its annotations: treatments & doses)
#       - From all data, collect vehicle-well data
#       - Re-express all data as percent of vehicle-well-in-column
#       - Output raw and normalized data, well by well, with annotations
#
# - Script was designed around 96wp CCNE1 HiBiT assay output, but could
#   normalize any 96wp RLU data acquired on a GloMax Discover:
#       - E.g., would be acceptable for normalizing CellTiter-Glo data, given
#         same plate layout
#



#
# Import necessary modules
#
import csv



#
# Define file I/O variables
#
data_file = "./data.csv"
annot_file = "./annot.csv"
doses_file = "./doses.csv"
output_file = "./output.csv"



#
# Open input file for reading, and collect raw measurements into a list ("all_rlu_data")
#
# ASSUME that experiment was conducted, and that measurements were collected, according to these rules:
#   - Data collected on a GloMax Discover instrument, with CSV output enabled: need CSV output!
#   - Rows in raw data file correspond to individual wells on the assay plate, iterating first by plate-column, then by plate-row
#       - This script was written to expect a CSV file as outputted by a GloMax Discover and its requisite software
#   - Assay was conducted on a 96w plate, and measurements were made accordingly
#       - This script written to expect that data was acquired using a GloMax Discover and its requisite software
#       - ASSUME no wells are excluded: input file should always have 97 rows, corresponding to (1x) label row + (96x) data rows
#   - Assay plate contains technical duplicates in adjacent columns (ie, 1+2, 3+4, 5+6 .. 11+12)
#   - (2x) technical replicates of (3x) doses: high to low, left to right
#
# ASSUME that input file adheres to these rules:
#   - File type is CSV
#   - First row contains labels
#   - Subsequent rows contain well-by-well data only, then file ends (ie, no additional rows at EoF)
#
with open(data_file, "r") as csvfile:
    reader = csv.reader(csvfile)

    # Pass through data-rows
    is_label_row = True
    all_rlu_data = []
    for row in reader:

        # Ignore first data-row (labels)
        if is_label_row:
            is_label_row = False

        else:

            # Only care about data-columns 2 ("WellPosition") and 5 ("RLU")
            well_id = row[2]
            well_rlu = float(row[5])
            all_rlu_data.append([well_id, well_rlu])

csvfile.close()



#
# From raw data list, collect vehicle control wells' RLU values
# Vehicle control wells are always located in plate-row A, with 12 plate-columns per plate-row
# Looking for data-rows where data-column 0 is ["A:1" .. "A:12"]
#
veh_rlu_data_row = []
for this_col in range(1,13):
    
    # Define the well ID we're looking for (ie, "A:xx")
    this_col_veh_well = "A:"+str(this_col)
    
    # Pass through all raw data, data-row by data-row
    for this_raw_data_row in all_rlu_data:

        # If data-row corresponds to the well ID we're looking for, collect its RLU value
        if this_raw_data_row[0] == this_col_veh_well:
            veh_rlu_data_row.append(this_raw_data_row[1])



#
# Next, construct a list of vehicle RLU data for each well on the plate
# Raw data list iterates well-by-well through the plate first by plate-column, then by plate-row
# Assay plate contains 8 plate-rows
# To construct vehicle RLU data list, iterate through the vehicle RLU data list 8 times (ie, one plate-column per plate-row)
#
veh_rlu_data = []
for i in range(0,8):
    for this_plate_row_veh_rlu in veh_rlu_data_row:
        veh_rlu_data.append(this_plate_row_veh_rlu)



#
# Next, get treatment labels
#
labels_list = []
with open(annot_file, "r") as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        labels_list.append(row[0])

csvfile.close()



#
# Then, flesh out labels to match each row of the data list
#
labels = []
for i in range(0,8):
    for j in range(0,6): labels.append(labels_list[i])
    for j in range(0,6): labels.append(labels_list[i+8])



#
# Next, get list of doses (expressed as uM)
#
doses_list = []
with open(doses_file, "r") as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        doses_list.append(row[0])

csvfile.close()

#
# Then, flesh out doses to match each row of the data list
#
doses = []
for k in range(0,16):
    for j in range(0,3):
        for i in range(0,2): doses.append(doses_list[j])



#
# Now, have everything we need to output normalized data
# Begin by opening output file and writing out a label row
#
with open(output_file, "w") as csvfile:
    writer = csv.writer(csvfile) 
    writer.writerow(["well_id", "treatment", "uM", "this_well_rlu", "this_well_veh_rlu", "pct_rlu_of_veh"])

    # For each measurement in the raw RLU table, normalize to the corresponding vehicle RLU measurement and write it out
    for this_well in range(0,96):

        # Express normalized data as percent of corresponding vehicle RLU measurement: (RLU_this_well) / (RLU_in_plate_colun_vehicle) * 100
        this_well_id = all_rlu_data[this_well][0]
        this_well_rlu = all_rlu_data[this_well][1]
        this_well_veh_rlu = veh_rlu_data[this_well]
        this_well_normalized = this_well_rlu / this_well_veh_rlu * 100
        this_well_label = labels[this_well]
        this_well_dose = doses[this_well]

        writer.writerow([this_well_id, this_well_label, this_well_dose, this_well_rlu, this_well_veh_rlu, this_well_normalized])



#
# Clean up for exit
#
csvfile.close()