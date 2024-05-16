import os
import pandas as pd
import time
import math
from src.magnetics import MagneticMaterial, MagneticDirichlet, MagneticVolumeIntegral
from src.femm_problem import FemmProblem
from src.general import LengthUnit
from src.geometry import Geometry, Line, Node
from src.executor import Executor
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from solenoid import solenoid

def getNodeInfo(file_path):

    struct_data = {}

    node_id = 0  # Initialize the runner variable for node identification
    current_node = None  # To hold the current node identifier during parsing

    with open(file_path,'r') as file:
        for line in file:
            line = line.strip()  # Clean up whitespace

            if 'Nodal results' in line:
                node_id += 1  # Increment node identifier on new section
                current_node = f"Node{node_id-1}"  # Format the current node ID as "Node0", "Node1", etc.
                continue

            # Split the line into components
            parts = line.split()
            if len(parts) < 5:
                continue  # Skip lines that do not have enough parts

            if current_node:
                x = float(parts[1].split(':')[1].replace(',',''))
                y = float(parts[2].split(':')[1].replace(',',''))
                if current_node not in struct_data:
                    struct_data[current_node] = {'x':x,'y':y}  # Initialize with coordinates

                # Join the parts for the physical variable name
                physical_var_name = ' '.join(parts[3:-2]).replace('=','').strip()
                physical_var_value = float(parts[-1])

                # Store the physical variable
                struct_data[current_node][physical_var_name] = physical_var_value
    return struct_data

def process_mesh_data(file_path):
    # Initialize the variables
    typeflag = 0
    nr_rows = None
    nr_nodes = None
    node_data = []
    block_data = []
    lines = []  # Use a list to collect lines first

    # Read the file and process it according to the given description
    with open(file_path,'r') as file:
        content = file.readlines()

        # tudjuk az előzményekből
        # Finding the row containing [ProblemType] and setting typeflag
        for index,line in enumerate(content):
            if '[ProblemType]' in line:
                if 'axisymmetric' in line.split('=')[-1].strip():
                    typeflag = 1
                break

        # Find the row with [Solution] in it
        for index,line in enumerate(content):
            if '[Solution]' in line:
                nr_rows = index
                nr_nodes = int(content[nr_rows + 1].strip())  # The line after noRow contains the number of nodes
                break

        # Le lehet kérni femm-ből
        # Parse node information if typeflag is 1
        if typeflag == 1 and nr_rows is not None:
            for i in range(nr_nodes):
                node_index = nr_rows + 2 + i
                parts = content[node_index].split()
                # N = i
                R = float(parts[0])
                Z = float(parts[1])
               # Re_A = float(parts[2])
               # Im_A = float(parts[3])
                node_data.append((R,Z)) #node_data.append((N,R,Z,complex(Re_A,Im_A)))

        # Find noBlock and parse block data
        if nr_rows is not None and nr_nodes is not None:
            noBlock_line_index = nr_rows + 2 + nr_nodes
            noBlock = int(content[noBlock_line_index].strip())

            for i in range(noBlock):
                block_index = noBlock_line_index + 1 + i
                parts = content[block_index].split()
                sorted_block = sorted([int(parts[0]),int(parts[1]),int(parts[2])])
                block_data.append(tuple(sorted_block))

                # Build lines and sort them, add to the list
                lines.append(tuple(sorted(sorted_block[:2])))
                lines.append(tuple(sorted(sorted_block[1:3])))
                lines.append(tuple(sorted([sorted_block[0],sorted_block[2]])))

    # Remove duplicates from lines by converting the list to a set and back to a list
    unique_lines = list(set(lines))

    # Return the results
    return node_data,block_data,unique_lines


def determine_properties_by_majority_rule(elements,node_properties):
    """ Determines the property of each element based on a majority rule and adjusts by neighbor influence only if needed. """
    # First, find the neighbors dynamically
    elements = {i:set(triangle) for i,triangle in enumerate(elements)}
    neighbors = find_neighbors(elements)

    element_properties = {}

    for elem_id,nodes in elements.items():
        # Count occurrences of each property in the current element
        property_count = {}
        for node in nodes:
            property = node_properties[node]
            if property in property_count:
                property_count[property] += 1
            else:
                property_count[property] = 1

        # Determine the property with the highest count (majority rule)
        max_property = max(property_count,key=property_count.get)
        element_properties[elem_id] = max_property

        # Check if all nodes in the element share the same property
        if len(property_count) == 1:
            continue  # Skip further checks and neighbor consideration

    # Adjust based on neighbors
    for elem_id,elem_neighbors in neighbors.items():
        if len(set(node_properties[n] for n in elements[elem_id])) > 1 and elem_neighbors:
            neighbor_properties = [element_properties[n] for n in elem_neighbors]
            property_count = {}
            for prop in neighbor_properties:
                if prop in property_count:
                    property_count[prop] += 1
                else:
                    property_count[prop] = 1

            majority_property = max(property_count,key=property_count.get)
            minority_property = min(property_count,key=property_count.get)

            # Apply rule based on neighbor majority
            if property_count[majority_property] == 2 and property_count[minority_property] == 1:
                element_properties[elem_id] = minority_property

    return element_properties


def export_nodal_values():


    return


if __name__ == '__main__':

    problem = solenoid(2, 2, 2, 6, 1)

    femm = Executor()
    current_dir = os.getcwd()
    lua_file = current_dir + "/solenoid.lua"
    femm.run(lua_file)

    # This script will starts with solenoid.ans to extract the nodal values
    file_path = current_dir + '/solenoid.ans'
    nodes, blocks, unique_lines = process_mesh_data(file_path)
    current_dir = os.getcwd()
    # k = math.ceil(len(nodes)/100)
    nodeInfo = {}

    # read values
    problem = FemmProblem(out_file="../meshextract.csv")
    problem.magnetic_problem(0, LengthUnit.CENTIMETERS, "axi")
    problem.openFem(current_dir + "\solenoid.fem")
    problem.load_specific_solution(current_dir + "/solenoid.ans")


    for node in nodes:
        problem.get_point_values(Node(node[0], node[1]))
    problem.close()
    problem.write("MeshExtract.lua")
    femm = Executor()
    lua_file = current_dir + "/MeshExtract.lua"
    femm.run(lua_file)
    file_path = "D:/PythonProjects/py2femm/examples/magnetics/meshextract.csv"
    nodeInfo.update(getNodeInfo(file_path))
    # Determine properties
    element_Sigma = determine_properties_by_majority_rule(blocks, [sub_dict['Sigma'] for sub_dict in nodeInfo.values()])
