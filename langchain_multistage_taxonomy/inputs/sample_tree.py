from treelib.tree import Tree
from treelib.node import Node

## MAKING A SAMPLE TREE! ##
# used as template input

class node_data:
    definition: str

    def __init__(self, definition):
        self.definition = definition

# Create a new tree
dummy_taxonomy_tree = Tree()

# Add root node
dummy_taxonomy_tree.create_node("root", "root")

# Add superclaims
dummy_taxonomy_tree.create_node(
    "WILDLIFE/ENVIRONMENT", "wild_env", parent="root", 
    data="Superclaim definition: Wind energy projects cause significant impacts - either positive or negative - to wildlife, ecosystems and/or the environment.")
dummy_taxonomy_tree.create_node(
    "HEALTH, SAFETY & LIVABILITY", "health", parent="root",
    data="Superclaim definition: Wind energy projects cause significant impacts - either positive or negative - to wildlife, ecosystems and/or the environment.")
dummy_taxonomy_tree.create_node("LOCAL COMMUNITY", "local_community", parent="root",
                                data="Superclaim definition: ...")

# Add subclaims
dummy_taxonomy_tree.create_node("WILDLIFE POPULATIONS", parent="wild_env", data="subclaim definition: ...")
dummy_taxonomy_tree.create_node("ECOSYSTEMS/PROTECTED AREAS", parent="wild_env", data="subclaim definition: ...")
dummy_taxonomy_tree.create_node("WASTE/POLLUTION", parent="wild_env", data="subclaim definition: ...")
dummy_taxonomy_tree.create_node("HEALTH & SAFETY", parent="health", data="subclaim definition: ...")

local_community_childs = [
    "LANDSCAPE, PROPERTY VALUE, & TOURISM",
    "LOCAL CONCERNS OVERLOOKED",
    "MINIMAL LOCAL ECONOMIC BENEFITS",
    "IDENTITY & CHARACTER OF COMMUNITY",
    "INDIGENOUS COMMUNITIES",
    "LAND DISPOSESSION",
    "RESIDENTIAL ABANDONMENT" 
]

for child in local_community_childs:
    dummy_taxonomy_tree.create_node(child, parent="local_community", data="subclaim definition: ...")

# Display the dummy_taxonomy_tree
try:
    dummy_taxonomy_tree.show(data_property="definition")
    # ^ note: for this to work, our node's data must be an object of 
    # node_data with field "definition". I didn't realize before, 
    # but this library function seems to be broken at the moment. 
    # however, it's possible to export the tree as a json as follows:
    
    # dummy_taxonomy_tree.to_json(with_data=True)
except:
    print("definitions not shown in tree.")
    dummy_taxonomy_tree.show()
