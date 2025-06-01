# Water Network Simulation with IRDM

It can be used for both steady-state and unsteady hydraulic simulations, enabling the analysis of valve maneuvers and leakage scenarios and their effects on flow and pressure throughout the network.

## ⚙️ Requirements

- Python 3.x  
- Required Python libraries:  
  - `wntr` (Water Network Tool for Resilience)  
  - `numpy`  
  - `matplotlib`  

You can install the required libraries using the following command:  
```bash
pip install wntr numpy matplotlib
```

## 📁 Input Files

The input for the simulation is an EPANET `.inp` file that defines the water network model. In the code, this file must be specified using the `inp` variable:  
```python
inp = r'path_to_your_file\network_file.inp'
```

## 🛠 Functions

- `f_dadosEpanet`: Extracts data from the EPANET `.inp` file, such as the number of pipes, nodes, and demands.  
- `f_permanente`: Performs the steady-state hydraulic analysis.  
- `f_transitorio`: Conducts the transient hydraulic analysis, including the simulation of valve maneuvers and leakage scenarios.  

## ⏳ Simulation Setup

The simulation parameters are configurable and defined in the code:
- **Time Step (`dt`)**: Simulation time step, in seconds.  
- **Steady-State Duration (`t_permanente`)**: Time for which the network is simulated under steady-state conditions before any maneuver.  
- **Maneuver Duration (`t_manobra`)**: Time during which a valve maneuver is simulated.  
- **Total Simulation Time (`t_simulacao`)**: Includes both steady-state and maneuver phases.

These parameters can be adjusted to match the scenario being analyzed.

## 🔁 Simulation Flow

1. Load the network data from the EPANET `.inp` file.  
2. Run the steady-state analysis for the system under normal conditions (without leakage).  
3. Simulate valve maneuvers by changing the valve coefficient (`k_manobra`) over time.  
4. Perform the transient analysis to evaluate how the maneuver affects flow and pressure.  
5. Introduce leakage at selected nodes and recompute the steady-state and transient behavior.  
6. Store and visualize the simulation results.

## ▶️ How to Run

1. Clone or download the repository.  
2. Place your EPANET `.inp` file in the working directory and set the `inp` path variable accordingly.  
3. Execute the Python script to run the simulation.

## 📊 Results

The simulation calculates the flow (`Qcal_lista`) and pressure head (`Hcal_lista`) at various points in the network throughout the simulation. Results are stored in dictionaries, organized by pipe and node IDs, which can be used for further analysis.

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for more details.
