import os

import femm
import math
import multiprocessing

import numpy as np
from tqdm import tqdm


# 1. Define pol2cart helper (assuming standard math)
def pol2cart(rho, phi_deg):
    """Converts polar coordinates (radius, degrees) to cartesian (x, y)."""
    phi_rad = math.radians(phi_deg)
    x = rho * math.cos(phi_rad)
    y = rho * math.sin(phi_rad)
    return x, y


# 2. Define the worker function
# This function must be self-contained for the separate process to run it.
def process_simulation(i):
    try:
        # Start a NEW instance of FEMM for this specific process
        # passing 1 hides the window to prevent UI clutter
        femm.openfemm(1)

        # Open the specific file
        femm.opendocument(f'fem/cog_{i}.fem')

        # User Logic
        femm.mi_selectgroup(9)
        femm.mi_moverotate(0, 0, i)

        # Run analysis (1 = minimized window)
        femm.mi_analyze(1)
        femm.mi_loadsolution()

        # Coordinate definitions
        coords_pol = [
            (4, 0), (7, 0), (21, 67.5 + i), (17, 80 + i), (17, 100 + i),
            (21, 115 + i), (17, 125 + i), (17, 145 + i), (21, 160 + i),
            (17, 170 + i), (17, -170 + i), (21, -160 + i), (17, -125 + i),
            (17, -145 + i), (21, -115 + i), (17, -80 + i), (17, -100 + i),
            (21, -67.5 + i), (17, -55 + i), (17, -35 + i), (21, -22.5 + i),
            (17, -10 + i), (17, 10 + i), (21, 22.5 + i), (17, 55 + i),
            (17, 35 + i)
        ]

        coords_cart = [pol2cart(j[0], j[1]) for j in coords_pol]

        for x, y in coords_cart:
            femm.mo_selectblock(x, y)

        # Calculate Torque
        wTorque_0 = femm.mo_blockintegral(22) * 1000

        # Clean up
        femm.mo_clearblock()
        femm.closefemm()  # Close this specific instance

        return wTorque_0

    except Exception as e:
        # Handle errors gracefully so one bad file doesn't crash the whole batch
        print(f"Error processing value {i}: {e}")
        try:
            femm.closefemm()
        except:
            pass
        return None


# 3. Main execution block
if __name__ == '__main__':
    # Define your values list here
    values = np.linspace(0,360,2048)

    femm.openfemm()
    femm.opendocument("steel_full_exc020_gl020.fem")

    os.mkdir("fem")
    for i in values:
        femm.mi_saveas(f'fem/cog_{i}.fem')
    femm.closefemm()

    # Check CPU count to determine number of workers
    num_processes = 8  # Leave one core for OS
    print(f"Starting simulation with {num_processes} processes...")

    # Clear the file initially (optional, or use 'a' to keep appending)
    with open("2D_FEMM_Steel_18mm_full_exc020_gl020.csv", "w") as f:
        pass

        # Use a Pool to manage processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Use imap (or imap_unordered) for iterative results and pass the iterator to tqdm
        # This is the line that generates the progress bar:
        results = list(tqdm(
            pool.imap(process_simulation, values),
            total=len(values),
            desc="FEMM Simulation Progress"
        ))

    # Write results to file in a single batch (avoids file locking issues)
    with open("2D_FEMM_Steel_18mm_full_exc020_gl020.csv", "a") as file_out:
        for res in results:
            if res is not None:
                file_out.write(f"{res}\n")

    print("Done.")