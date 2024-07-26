import sys
import numpy as np

class CollNode:
    def __init__(self):
        self.id = -1                   # id of this particle
        self.mass = -1.0               # Mass of this particle
        self.children = []             # Nodes corresponding to previous collisions
        self.parent = None             # Node corresponding to next collision of this particle
        self.parent_time = sys.maxsize # Time at which this node connected to the parent

# The root is an empty node.
# Children of the root represent particles that survived until the
# end of the simulation.
class CollisionTree:
    def __init__(self, df):
        self.root = CollNode()

        for idx, row in df.iterrows():
            self.add(row)
        
    def find_rec(self, id, node):
        if node.id == id:
            return node
        
        elif node.children:
            for child in node.children:
                result = self.find_rec(id, child)
                if result:
                    return result

    def find(self, id):
        return self.find_rec(id, self.root)

    def add(self, row):
        s_id, d_id, coll_time = row['s_id'], row['d_id'], row['time']
        if s_id == row['indexi']:
            s_mass = row['mi']
            d_mass = row['mj']
        else:
            s_mass = row['mj']
            d_mass = row['mi']

        s_node = self.find(s_id)

        # This particle does not yet exist in the tree
        # Create a new subtree and attach to the root
        if s_node == None:
            s_node = CollNode()
            s_node.id = s_id
            s_node.mass = s_mass
            s_node.parent = self.root
            s_node.parent_time = coll_time
            self.root.children.append(s_node)

        d_node = CollNode()
        d_node.id = d_id
        d_node.mass = d_mass
        d_node.parent = s_node
        d_node.parent_time = coll_time
        
        s_node.children.append(d_node)

    def get_tree_mass(self, node):
        if not node.children:
            return node.mass
        
        return sum(self.get_tree_mass(child) for child in node.children)