# Neuron Activity Simulator 

## Day 03 – Python Assignment

### Project Description

This project simulates neuronal activity using the Leaky Integrate-and-Fire (LIF) model.

The goal is to investigate how different electrical input patterns affect neuronal firing.

### Neuron Activity Patterns

The program simulates three types of neuronal activity:

1. **Burst Firing:** A neuron that fires multiple action potentials in short bursts, followed by periods of silence.
2. **Periodic Firing:** A neuron that fires approximately once every 4 seconds.
3. **Inhibited Neuron:** A neuron receiving inhibitory input, resulting in very little neuronal firing.

### Scientific Background

The Leaky Integrate-and-Fire model describes how a neuron's membrane potential changes in response to electrical input.

The resting membrane potential is -70 mV, and the firing threshold is -55 mV.

When the membrane potential reaches the threshold, a spike is recorded and the membrane potential resets to -70 mV.

### Python Implementation

The program:

- Reads electrical stimulus data from CSV files.
- Calculates membrane potential changes using the LIF model.
- Detects action potentials.
- Creates animated visualizations of three neurons.
- Displays membrane potential graphs.
- Saves simulation results to CSV files.

### Files

- `main.py` – Main simulation program.
- `stimuli_burst.csv` – Burst firing stimulus data.
- `stimuli_periodic_4s.csv` – Periodic stimulus data.
- `stimuli_inhibited.csv` – Inhibitory stimulus data.
- `results_*.csv` – Simulation results.

### How to Run

Install Matplotlib:

```bash
python -m pip install matplotlib
```

Run the program:

```bash
python main.py
```

### Conclusion

This project demonstrates how different electrical input patterns influence neuronal firing. Stronger excitatory inputs can increase firing frequency, while inhibitory inputs can suppress neuronal activity.

The simulation is a simplified computational model and does not reproduce all biological properties of real neurons.
