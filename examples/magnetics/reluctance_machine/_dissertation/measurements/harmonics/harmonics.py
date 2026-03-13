import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.interpolate import interp1d


def calculate_spectrum(angle_data, torque_data, N=8192):
    """
    Helper function to calculate the FFT spectrum of a torque signal.
    Returns: (harmonics_orders, amplitude_array)
    """
    # Ensure data is sorted by angle
    sorted_indices = np.argsort(angle_data)
    angle_sorted = angle_data[sorted_indices]
    torque_sorted = np.array(torque_data)[sorted_indices]

    # Resample to uniform spacing over exactly 0 to 360 degrees
    uniform_angle = np.linspace(0, 360, N, endpoint=False)

    # Interpolate measurement onto this uniform grid
    interpolator = interp1d(angle_sorted, torque_sorted, kind='linear', fill_value="extrapolate")
    uniform_torque = interpolator(uniform_angle)

    # Remove DC Offset (Mean)
    uniform_torque = uniform_torque - np.mean(uniform_torque)

    # Perform FFT
    yf = rfft(uniform_torque)
    xf = rfftfreq(N, 1 / N)  # Frequencies in "cycles per revolution"

    # Normalize Amplitude
    amplitude = 2.0 / N * np.abs(yf)

    return xf, amplitude


def compare_torque_harmonics(meas_angle, meas_torque, sim_angle, sim_torque, slots, poles):
    """
    Plots side-by-side FFT bars for Measured vs Simulated data.
    """
    # Calculate Spectra for both
    xf_meas, amp_meas = calculate_spectrum(meas_angle, meas_torque)
    xf_sim, amp_sim = calculate_spectrum(sim_angle, sim_torque)

    # Scale amplitudes to mNm
    amp_meas_mnm = amp_meas * 1000
    amp_sim_mnm = amp_sim * 1000

    # --- PLOTTING ---
    fig, ax = plt.subplots(figsize=(8, 6))

    lcm_val = np.lcm(slots, poles)
    # Ensure we calculate enough orders to fill the 0-100 view, or the original max_order if larger
    max_order = max(100, int(lcm_val * 2.5))

    # Slice arrays to max_order for plotting
    orders = xf_meas[:max_order]  # Assuming xf is same for both since N is constant

    colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
              "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

    # Bar Plotting (Side by Side)
    width = 0.35
    ax.bar(orders - width / 2, amp_meas_mnm[:max_order], width=width, color=colors[0], label='Measurement')
    ax.bar(orders + width / 2, amp_sim_mnm[:max_order], width=width, color=colors[2], label='Simulation')

    ax.set_xlabel('Harmonic Order (Cycles per Revolution)', fontsize=18)
    ax.set_ylabel('Torque Amplitude (mNm)', fontsize=18)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    # Set X-axis limit to 0-100 as requested
    ax.set_xlim(0, 100)

    ax.legend(fontsize=18)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('harmonics.png', dpi=300)
    plt.show()

    # Print Comparison Table for Key Harmonics
    print(f"{'Order':<10} | {'Measured (mNm)':<15} | {'Simulated (mNm)':<15} | {'Diff':<10}")
    print("-" * 55)
    key_orders = [1, poles, slots, lcm_val, lcm_val * 2, lcm_val * 3, lcm_val * 4]
    for order in key_orders:
        idx = int(order)  # Index corresponds to order because xf steps by 1
        m_val = amp_meas_mnm[idx]
        s_val = amp_sim_mnm[idx]
        print(f"{order:<10} | {m_val:.4f}          | {s_val:.4f}          | {m_val - s_val:.4f}")


# --- DATA PROCESSING & EXECUTION ---

# Configuration
SLOTS = 12
POLES = 8

# 1. Load Measured Data
try:
    meas_df = pd.read_csv('measurement_filtered.csv')
    measured_torque = meas_df.iloc[:, 1].values.flatten().tolist()
    # Generate angle array 0-360 based on data length
    raw_angle_meas = np.linspace(0, 360, len(measured_torque), endpoint=False)
    print("Measurement data loaded.")
except FileNotFoundError:
    print("Error: 'measurement_filtered.csv' not found. Creating dummy data.")
    measured_torque = np.random.normal(0, 0.1, 3600)
    raw_angle_meas = np.linspace(0, 360, 3600)

# 2. Load & Process Simulation Data
try:
    sim = pd.read_csv('2D_FEMM_Steel_18mm_full_base.csv')


    # Rotation Helper
    def rotate(arr, k=0):
        k %= len(arr)
        return arr[-k:] + arr[:-k]


    base = list(sim["torque"])
    # Apply user-defined rotation
    skew1 = rotate(list(sim["torque"]), -64)

    # Combine and Scale (User Logic)
    simulation_data = rotate([(i + j) / 1000 for i, j in zip(base, skew1)], 0)

    # Generate angle array 0-360 for simulation
    raw_angle_sim = np.linspace(0, 360, len(simulation_data), endpoint=False)
    print("Simulation data loaded and processed.")

except FileNotFoundError:
    print("Error: '2D_FEMM_Steel_18mm_full_base.csv' not found. Creating dummy data.")
    simulation_data = np.random.normal(0, 0.05, 3600)
    raw_angle_sim = np.linspace(0, 360, 3600)

# 3. Run Comparison
compare_torque_harmonics(raw_angle_meas, measured_torque, raw_angle_sim, simulation_data, SLOTS, POLES)