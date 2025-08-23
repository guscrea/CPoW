# this script takes a spreadsheet of hierarchical claims & imports it as a tree of root -> superclaims -> sublaims. Definition of each claim is saved in node in "data" field
# see sample_tree.py for example of tree output.

# TODO: modify code so any depth of hierarchy can be imported.

# (we use a .csv file instead of a Google Sheet because Brown admin prevents students from using the Googl Sheets API.)

import csv
import logging
import sys
from treelib.tree import Tree

# error logging:
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                     level=logging.INFO, stream=sys.stdout)

# TODO: iterate through tree. for each subclaim, attach it to superclaim node OR make superclaim node.

filename = "inputs/22_8_25_cpow_taxonomy.csv"  # File name - configurable
col_index = { # zero-indexing; configurable
    "superclaim": 3,
    "superclaim_def": 4, 
    "subclaim": 1,
    "subclaim_def": 2
}
fields = []  # Column names
rows = []    # Data rows

logging.info(f'extracting taxonomy tree from file name: {filename}! \n')

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)  # Reader object

    fields = next(csvreader)  # Read header
    for row in csvreader:     # Read rows
        rows.append(row)

logging.info(f"csv fields: {fields} \n")
logging.info(f"first 3 rows of {csvreader.line_num}: {rows[:3]} \n")

wind_tree = Tree()

# Add root node
wind_tree.create_node("root", "root")

# add claims & subclaims w/ definitions
for row in rows:
    parent = row[col_index["superclaim"]]
    if not wind_tree.contains(parent): 
        # to be safer, this should check whether parent 
        # appears in tree level directly above the node we're about to insert - 
        # but I don't think this edge case will come up.
        wind_tree.create_node(tag=parent, identifier=parent,
                              parent="root",
                              data={"def": col_index["superclaim_def"]})
    wind_tree.create_node(
        tag=row[col_index["subclaim"]],
        identifier=row[col_index["subclaim"]],
        parent=parent,
        data={"definition": col_index["subclaim_def"]}
    )

    wind_tree.show()

    # json_with_data = wind_tree.to_json(with_data=True)
    # print(json_with_data)