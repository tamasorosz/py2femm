def getNodeInfo(file_path):

    struct_data = {}

    node_id = 0  # Initialize the runner variable for node identification
    current_node = None  # To hold the current node identifier during parsing

    with open(file_path,'r') as file:
        for line in file:
            line = line.strip()  # Clean up whitespace

            if 'Point values' in line:
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


# Path to the file
file_path = 'solenoid.ans'

# Initialize the variables
typeflag = 0
noRow = None
noNod = None
node_data = []
block_data = []
lines_data = set()


# Function to determine if two line segments are unique
def add_unique_line(p1,p2):
    if (p1,p2) not in lines_data and (p2,p1) not in lines_data:
        lines_data.add((p1,p2))



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
            N = i
            R = float(parts[0])
            Z = float(parts[1])
            Re_A = float(parts[2])
            Im_A = float(parts[3])
            node_data.append((N,R,Z,complex(Re_A,Im_A)))

    # Find noBlock and parse block data
    if noRow is not None and noNod is not None:
        noBlock_line_index = noRow + 2 + noNod
        noBlock = int(content[noBlock_line_index].strip())  # Correctly fetching noBlock from the file

        for i in range(noBlock):
            block_index = noBlock_line_index + 1 + i
            parts = content[block_index].split()
            P1,P2,P3 = int(parts[0]),int(parts[1]),int(parts[2])
            block_data.append((P1,P2,P3))
            # Add unique lines
            add_unique_line(P1,P2)
            add_unique_line(P2,P3)
            add_unique_line(P3,P1)