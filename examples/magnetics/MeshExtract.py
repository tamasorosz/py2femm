import os
from meshTopology import getNodeInfo
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
from scipy.linalg import cholesky



def process_mesh_data(file_path):
    # Initialize the variables
    typeflag = 0
    noRow = None
    noNod = None
    node_data = []
    block_data = []
    lines = []  # Use a list to collect lines first

    # Read the file and process it according to the given description
    with open(file_path,'r') as file:
        content = file.readlines()

        # Finding the row containing [ProblemType] and setting typeflag
        for index,line in enumerate(content):
            if '[ProblemType]' in line:
                if 'axisymmetric' in line.split('=')[-1].strip():
                    typeflag = 1
                break

        # Find the row with [Solution] in it
        for index,line in enumerate(content):
            if '[Solution]' in line:
                noRow = index
                noNod = int(content[noRow + 1].strip())  # The line after noRow contains the number of nodes
                break

        # Parse node information if typeflag is 1
        if typeflag == 1 and noRow is not None:
            for i in range(noNod):
                node_index = noRow + 2 + i
                parts = content[node_index].split()
                # N = i
                R = float(parts[0])
                Z = float(parts[1])
               # Re_A = float(parts[2])
               # Im_A = float(parts[3])
                node_data.append((R,Z)) #node_data.append((N,R,Z,complex(Re_A,Im_A)))

        # Find noBlock and parse block data
        if noRow is not None and noNod is not None:
            noBlock_line_index = noRow + 2 + noNod
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


def find_neighbors(elements):
    """ Finds the neighbors of each element based on shared nodes. """

    neighbors = {elem_id:[] for elem_id in elements}
    for elem_id1,nodes1 in elements.items():
        for elem_id2,nodes2 in elements.items():
            if elem_id1 != elem_id2 and len(set(nodes1) & set(nodes2)) >= 2:
                neighbors[elem_id1].append(elem_id2)
                if len(neighbors[elem_id1]) == 3:  # No more than 3 neighbors in 2D triangular meshes
                    break
    return neighbors


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


def triangleArea(x1, x2, x3, y1, y2, y3):
    """
    Calculate the area of a triangle given its vertex coordinates using the shoelace formula.
    The result is scaled according to the unit of measure.

    Parameters:
        x1, x2, x3, y1, y2, y3: Coordinates of the triangle vertices.
        unit_scale (float): Scaling factor for units (e.g., 1 for meters, 0.01 for centimeters).

    Returns:
        float: The area of the triangle scaled by the unit of measure.
    """
    A = 0.5 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    return A


def ensureCounterclockwise(x1,x2,x3,y1,y2,y3):
    """
    Ensure that the triangle vertices are ordered in a counterclockwise direction.
    If not, swap the second and third vertices to make them counterclockwise.

    Returns:
        tuple: The potentially reordered coordinates and a boolean flag indicating if a swap occurred.
    """
    # Calculate the cross product to determine the order of the points
    cross_product = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

    if cross_product < 0:
        # Points are in clockwise order, so swap the second and third vertices
        x2,x3 = x3,x2
        y2,y3 = y3,y2
        swap_occurred = True
    else:
        swap_occurred = False

    return (x1,x2,x3,y1,y2,y3),swap_occurred

def Kij_matrix(nodes,nodeInfo,block_data,unit_scale):
    element_Mu = determine_properties_by_majority_rule(block_data,[sub_dict['Mux'] for sub_dict in nodeInfo.values()])
    ii=0
    K_glb = np.zeros((len(nodes),len(nodes)))
    for currentBlock in block_data:
        x1 = unit_scale*(nodes[currentBlock[0]][0])
        x2 = unit_scale*(nodes[currentBlock[1]][0])
        x3 = unit_scale*(nodes[currentBlock[2]][0])
        y1 = unit_scale*(nodes[currentBlock[0]][1])
        y2 = unit_scale*(nodes[currentBlock[1]][1])
        y3 = unit_scale*(nodes[currentBlock[2]][1])
        (x1,x2,x3,y1,y2,y3),swap_occurred = ensureCounterclockwise(x1,x2,x3,y1,y2,y3)
        if swap_occurred:
            currentBlock = [currentBlock[0], currentBlock[2], currentBlock[1]]
        A = triangleArea(x1,x2,x3,y1,y2,y3)
        yjk = y2 - y3
        yij = y1 - y2
        yki = y3 - y1

        xji = x2 - x1
        xkj = x3 - x2
        xik = x1 - x3

        # Calculate the stiffness matrix entries K_ij
        K = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
        nu = 1/element_Mu[ii]
        K[0][0] = nu * (yjk * yjk + xkj * xkj) / (4 * A)
        K[0][1] = nu * (yjk * yki + xkj * xik) / (4 * A)
        K[0][2] = nu * (yjk * yij + xkj * xji) / (4 * A)
        K[1][0] = K[0][1]
        K[1][1] = nu * (yki * yki + xik * xik) / (4 * A)
        K[1][2] = nu * (yki * yij + xik * xji) / (4 * A)
        K[2][0] = K[0][2]
        K[2][1] = K[1][2]
        K[2][2] = nu * (yij * yij + xji * xji) / (4 * A)
        ii +=1
        # Assemble local stiffness matrix into global stiffness matrix
        for i in range(3):
            for j in range(3):
                K_glb[currentBlock[i],currentBlock[j]] += K[i][j]
    return K_glb


def Nij_matrix(nodes,node_info,block_data,unit_scale):
    element_sigma = determine_properties_by_majority_rule(block_data,
                                                          [sub_dict['Sigma'] for sub_dict in node_info.values()])
    K_glb = np.zeros((len(nodes),len(nodes)))

    for ii,current_block in enumerate(block_data):
        x1 = unit_scale * nodes[current_block[0]][0]
        x2 = unit_scale * nodes[current_block[1]][0]
        x3 = unit_scale * nodes[current_block[2]][0]
        y1 = unit_scale * nodes[current_block[0]][1]
        y2 = unit_scale * nodes[current_block[1]][1]
        y3 = unit_scale * nodes[current_block[2]][1]

        (x1,x2,x3,y1,y2,y3),swap_occurred = ensureCounterclockwise(x1,x2,x3,y1,y2,y3)
        if swap_occurred:
            current_block = [current_block[0],current_block[2],current_block[1]]

        A = triangleArea(x1,x2,x3,y1,y2,y3)

        # Calculate the local stiffness matrix entries T_ij
        sigma = element_sigma[ii]
        T = np.zeros((3,3))
        T[0,0] = sigma * A / 6
        T[0,1] = T[1,0] = sigma * A / 12
        T[0,2] = T[2,0] = sigma * A / 12
        T[1,1] = sigma * A / 6
        T[1,2] = T[2,1] = sigma * A / 12
        T[2,2] = sigma * A / 6

        # Assemble local stiffness matrix into global stiffness matrix
        for i in range(3):
            for j in range(3):
                K_glb[current_block[i],current_block[j]] += T[i][j]

    return K_glb

if __name__ == '__main__':
    # Extract node information using py2femm
    # Path to the file
    file_path = 'solenoid.ans'
    nodes,blocks,unique_lines = process_mesh_data(file_path)
    current_dir = os.getcwd()
    # k = math.ceil(len(nodes)/100)
    nodeInfo = {}
    problem = FemmProblem(out_file="meshextract.csv")
    problem.magnetic_problem(0,LengthUnit.CENTIMETERS,"axi")
    problem.openFem(current_dir + "/solenoid/solenoid.fem")
    problem.load_specific_solution(current_dir + "/solenoid.ans")
    for node in nodes:
        problem.get_point_values(Node(node[0],node[1]))
    problem.close()
    problem.write("MeshExtract.lua")
    femm = Executor()
    lua_file = current_dir + "/MeshExtract.lua"
    femm.run(lua_file)
    file_path = current_dir +"/meshextract.csv"
    nodeInfo.update(getNodeInfo(file_path))
 # Determine properties
    element_Sigma = determine_properties_by_majority_rule(blocks,[sub_dict['Sigma'] for sub_dict in nodeInfo.values()])

# df = pd.DataFrame.from_dict(nodeInfo)
# df.to_excel('asdgqvqv.xlsx', index=False)
    K_glb = Kij_matrix(nodes,nodeInfo,blocks,0.01)
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    x = np.arange(K_glb.shape[0])
    y = np.arange(K_glb.shape[1])
    x,y = np.meshgrid(x,y)
    z = K_glb[x,y]

    ax.plot_surface(x,y,z,cmap='viridis')
    ax.set_title('Surface Plot of Global Stiffness Matrix K_glb')
    ax.set_xlabel('Node Index')
    ax.set_ylabel('Node Index')
    ax.set_zlabel('Value')

    plt.show()
    # Assertions
    main_diagonal = np.diag(K_glb)
    assert np.all(main_diagonal > 0),"Not all diagonal elements are positive."

    import numpy as np
    from scipy.linalg import cholesky


    def is_positive_definite(matrix):
        """Check if the matrix is positive definite using Cholesky decomposition."""
        try:
            _ = cholesky(matrix)
            return True
        except np.linalg.LinAlgError:
            return False


    def is_diagonally_dominant(matrix, tolerance=0.0001):
        """Check if the matrix is diagonally dominant with a given tolerance."""
        D = np.abs(matrix.diagonal())
        S = np.sum(np.abs(matrix), axis=1) - D
        # Apply the tolerance
        return D, S, np.all(D >= (1 - tolerance) * S)


    def check_stiffness_matrix(matrix, tolerance=0.0001):
        """Check if the matrix is positive definite and diagonally dominant."""
        pos_def = is_positive_definite(matrix)
        D, S, diag_dom = is_diagonally_dominant(matrix, tolerance)

        if not diag_dom:
            print("Warning: The stiffness matrix is not diagonally dominant at the following nodes (with tolerance):")
            for i in range(len(D)):
                if D[i] < (1 - tolerance) * S[i]:
                    difference = S[i] - D[i]
                    percentage_difference = (difference / S[i]) * 100
                    print(
                        f"Node {i + 1}: D = {D[i]}, Sum off-diag = {S[i]}, Diff= {difference} ({percentage_difference:.2f}%)")
        if not pos_def and not diag_dom:
            print("Warning: The stiffness matrix is neither positive definite nor diagonally dominant.")
        elif not pos_def:
            print("Warning: The stiffness matrix is not positive definite.")
        elif diag_dom:
            print("The stiffness matrix is diagonally dominant (with tolerance).")

        return pos_def, diag_dom


print("Checking matrix:")
pos_def, diag_dom = check_stiffness_matrix(K_glb)
print(f"Positive Definite: {pos_def}")
print(f"Diagonally Dominant: {diag_dom}")
print(f"Symmetric: {np.allclose(K_glb, K_glb.T, atol=1e-6)}\n")
N_glb =Nij_matrix(nodes,nodeInfo,blocks,0.01)
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
x = np.arange(N_glb.shape[0])
y = np.arange(N_glb.shape[1])
x,y = np.meshgrid(x,y)
z = N_glb[x,y]
ax.plot_surface(x,y,z,cmap='viridis')
ax.set_title('Surface Plot of Global Matrix N_glb')
ax.set_xlabel('Node Index')
ax.set_ylabel('Node Index')
ax.set_zlabel('Value')

plt.show()
    # assert np.all(off_diagonal <= 0),"Not all off-diagonal elements are non-positive."
a = 0