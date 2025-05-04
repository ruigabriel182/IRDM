# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 07:13:08 2023

@author: RUI GABRIEL
"""

# MAIN LIBRARIES IMPORT
import wntr                          # WNTR library for water network modeling and simulation
import numpy as np                   # NumPy for numerical operations
import time                          # Time tracking
import matplotlib.pyplot as plt      # For plotting graphs

# SUPPORT MODULES IMPORT
import f_dadosEpanet as fd           # Functions to extract EPANET data
import f_permanente as fp            # Functions for steady-state analysis
import f_transitorio as frt          # Functions for transient (unsteady) analysis

start_time = time.time()             # Start timer to track total execution time

#%% INPUTS

# Load the EPANET .inp file representing the network to be analyzed
inp = r'C:\Users\ruig1\OneDrive\0. DOUTORADO\MDIR - V3\GITHUB\modena2_SemVazamento.inp' 
rede = wntr.network.WaterNetworkModel(inp)  # Create a water network model from the file

# Extract general data: number of pipes, nodes, demands (RNF/RNV), valves and pumps
nTubo, nNo, nRNF, nRNV, nValvula, nBomba = fd.numero_dados(rede)

# Collect detailed objects from the network
tubo, no, rnf, valvula, bomba = fd.coletar_dados(rede)

# SIMULATION TIME SETTINGS
dt = .05  # Time step in seconds
t_permanente = 2  # Duration of steady-state phase before transient event (s)
t_manobra = 15  # Duration of valve maneuver (s)
t_simulacao = t_manobra + t_permanente + 3  # Total simulation time (s)
k_f = 110  # Final valve resistance coefficient after maneuver
tempo_total = np.arange(0, t_simulacao, dt)  # Time vector for the whole simulation

# Define how long the maneuver lasts in number of time steps
t_manobra_indices = int(t_manobra / dt)

# Initialize k_manobra vector (valve coefficient over time)
k_manobra = np.zeros_like(tempo_total)

# Set valve coefficient (k) during simulation:
k_manobra[0:int(t_permanente)] = 0  # Before maneuver: k = 0
k_manobra[int(t_permanente / dt):int(t_permanente / dt) + t_manobra_indices] = np.interp(
    np.arange(t_permanente, t_permanente + t_manobra, dt),
    [t_permanente, t_permanente + t_manobra],
    [0, k_f])  # Linearly increase k during maneuver
k_manobra[int(t_permanente / dt) + t_manobra_indices:] = k_f  # After maneuver: constant k

# Define pump rotation (not used here, but prepared)
n_i = 1  # Initial rotation factor
n_f = 1  # Final rotation factor
n_rotacao = np.zeros_like(tempo_total)

# Set pump rotation over time
n_rotacao[0:int(t_permanente / dt)] = n_i
n_rotacao[int(t_permanente / dt):int(t_permanente / dt) + t_manobra_indices] = np.interp(
    np.arange(t_permanente, t_permanente + t_manobra, dt),
    [t_permanente, t_permanente + t_manobra],
    [n_i, n_f])  # Interpolate rotation if needed
n_rotacao[int(t_permanente / dt) + t_manobra_indices:] = n_f

# Plot the valve coefficient (k) evolution during the maneuver
plt.plot(tempo_total, k_manobra)
plt.xlabel('Time (s)')
plt.ylabel('k_manobra')
plt.title('k variation during maneuver')
plt.grid(True)
plt.show()

# List all pipe and node indices (used later for maneuvers)
tubo_manobra_index = [tubo[i].index for i in range(nTubo)]  # Include all pipe indices (adjust if necessary)
no_manobra_index = [no[i].index for i in range(nNo)]        # Include all node indices (adjust if necessary)

#%% WITHOUT LEAKAGE

# Compute the steady-state initial condition (no leaks)
Qcal_lista, Hcal_lista, A10, A12, A21, D, H0, no_idx_vazamento = fp.regime_permanente(
    rede, nTubo, nNo, nRNF, nRNV, nValvula, nBomba, tubo, no, rnf, valvula, bomba)

# Store the final steady-state results
Hpermanente = Hcal_lista[-1]  # Head at final steady-state
Qpermanente = np.array(Qcal_lista[-1])  # Flow at final steady-state

Manobra_semvazamento = {}  # Dictionary to store results without leak

# Loop through each pipe index to simulate a maneuver
for i in tubo_manobra_index:

    tubo_manobra = i                 # Pipe to be maneuvered
    bomba_manobra = 1000000         # Placeholder value (not using pumps here)

    # Perform transient simulation for current maneuver
    Qcal_lista, Hcal_lista = frt.regime_transitorio(
        rede, Qpermanente, A10, A12, A21, D, H0, no_idx_vazamento,
        dt, t_simulacao, k_manobra, tubo_manobra, n_rotacao,
        bomba_manobra, nTubo, nNo, nRNF, nRNV, nValvula, nBomba,
        tubo, no, rnf, valvula, bomba)

    Hcal_lista[0] = Hpermanente  # Ensure initial head matches steady-state

    # Store results by pipe ID
    Manobra_semvazamento[tubo[i].ID] = {
        'Qcal_lista': Qcal_lista,
        'Hcal_lista': Hcal_lista}

    print(f"\nManeuver Pipe ID P{i + 1}", end="\r")  # Progress update

#%% WITH LEAKAGE

No_comvazamento = {}  # Dictionary to store results for each leakage location

# Loop through each node to simulate leakage
for j in no_manobra_index:

    no[j].Cd = 0.33 / 1000  # Set leak coefficient at node
    # Recalculate steady-state with leak
    Qcal_lista, Hcal_lista, A10, A12, A21, D, H0, no_idx_vazamento = fp.regime_permanente(
        rede, nTubo, nNo, nRNF, nRNV, nValvula, nBomba, tubo, no, rnf, valvula, bomba)
    Hpermanente = Hcal_lista[-1]
    Qpermanente = np.array(Qcal_lista[-1])

    Manobra_comvazamento = {}  # Store results for each maneuver with leak

    # Loop through each pipe to simulate maneuvers
    for i in tubo_manobra_index:

        tubo_manobra = i
        bomba_manobra = 1000000

        Qcal_lista, Hcal_lista = frt.regime_transitorio(
            rede, Qpermanente, A10, A12, A21, D, H0, no_idx_vazamento,
            dt, t_simulacao, k_manobra, tubo_manobra, n_rotacao,
            bomba_manobra, nTubo, nNo, nRNF, nRNV, nValvula, nBomba,
            tubo, no, rnf, valvula, bomba)

        Hcal_lista[0] = Hpermanente  # Set initial head

        # Store results by pipe ID
        Manobra_comvazamento[tubo[i].ID] = {
            'Qcal_lista': Qcal_lista,
            'Hcal_lista': Hcal_lista}

    # Print progress for current leak node
    tempo_decorrido = time.time() - start_time
    minutos, segundos = divmod(int(tempo_decorrido), 60)
    horas, minutos = divmod(minutos, 60)
    print(f"\nLeakage at Node ID N{j + 1}", end="\r")

    no[j].Cd = None  # Reset leak coefficient to None
    No_comvazamento[no[j].ID] = Manobra_comvazamento  # Store all maneuvers for this leak node

# Final time log
end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nTotal elapsed time: {elapsed_time:.5f} seconds")