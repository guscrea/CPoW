from treelib.tree import Tree

## MAKING A SAMPLE TREE! ##

# Create a new tree
dummy_taxonomy_tree = Tree()

# Add root node
dummy_taxonomy_tree.create_node("root", "root")

# Add superclaims
dummy_taxonomy_tree.create_node("WILDLIFE/ENVIRONMENT", "wild_env", parent="root")
dummy_taxonomy_tree.create_node("HEALTH, SAFETY & LIVABILITY", "health", parent="root")
dummy_taxonomy_tree.create_node("LOCAL COMMUNITY", "local_community", parent="root")

# Add subclaims
dummy_taxonomy_tree.create_node("WILDLIFE POPULATIONS", parent="wild_env")
dummy_taxonomy_tree.create_node("ECOSYSTEMS/PROTECTED AREAS", parent="wild_env")
dummy_taxonomy_tree.create_node("WASTE/POLLUTION", parent="wild_env")
dummy_taxonomy_tree.create_node("HEALTH & SAFETY", parent="health")

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
    dummy_taxonomy_tree.create_node(child, parent="local_community")

# Display the dummy_taxonomy_tree
dummy_taxonomy_tree.show()