
import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle


# ==========================================
# FILE PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

STIMULI_FILE = BASE_DIR / "stimuli.csv"
RESULTS_FILE = BASE_DIR / "results.csv"
GRAPH_FILE = BASE_DIR / "neuron_activity.png"


# ==========================================
# NEURON PARAMETERS
# ==========================================

RESTING_POTENTIAL = -70.0  # mV
THRESHOLD = -55.0          # mV
RESET_POTENTIAL = -70.0    # mV
TIME_CONSTANT = 10.0       # ms
RESISTANCE = 1.0           # MOhm
DT = 1.0                   # ms


# ==========================================
# CREATE STIMULUS DATA
# ==========================================

def create_stimuli_file():
    """Create example electrical stimuli if missing."""

    if STIMULI_FILE.exists():
        return

    print("Creating stimuli.csv...")

    with open(STIMULI_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["current"])

        for time in range(200):

            if time < 40:
                current = 0
            elif time < 90:
                current = 30
            elif time < 140:
                current = 50
            elif time < 170:
                current = 10
            else:
                current = 40

            writer.writerow([current])


def load_stimuli():
    """Load electrical currents from CSV."""

    currents = []

    with open(STIMULI_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            currents.append(float(row["current"]))

    return currents


# ==========================================
# LEAKY INTEGRATE-AND-FIRE MODEL
# ==========================================

def update_voltage(voltage, current):
    """Calculate the next membrane voltage."""

    change = (DT / TIME_CONSTANT) * (
        RESTING_POTENTIAL
        - voltage
        + RESISTANCE * current
    )

    return voltage + change


def simulate_neuron(currents):
    """Simulate voltage changes and detect spikes."""

    voltage = RESTING_POTENTIAL

    times = []
    voltages = []
    spike_times = []

    for step, current in enumerate(currents):

        time = step * DT

        voltage = update_voltage(voltage, current)

        if voltage >= THRESHOLD:
            spike_times.append(time)
            voltage = RESET_POTENTIAL

        times.append(time)
        voltages.append(voltage)

    return times, voltages, spike_times


# ==========================================
# SAVE RESULTS
# ==========================================

def save_results(times, voltages, spike_times):
    """Save simulation results to CSV."""

    spike_set = set(spike_times)

    with open(RESULTS_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["time_ms", "voltage_mv", "spike"])

        for time, voltage in zip(times, voltages):

            spike = 1 if time in spike_set else 0

            writer.writerow([
                time,
                round(voltage, 2),
                spike
            ])


# ==========================================
# PLOT MEMBRANE POTENTIAL
# ==========================================

def plot_results(times, voltages, spike_times):
    """Plot membrane potential and firing events."""

    fig, ax = plt.subplots(figsize=(11, 5))

    ax.plot(
        times,
        voltages,
        color="blue",
        label="Membrane potential"
    )

    ax.axhline(
        THRESHOLD,
        color="red",
        linestyle="--",
        label="Firing threshold (-55 mV)"
    )

    ax.axhline(
        RESTING_POTENTIAL,
        color="green",
        linestyle=":",
        label="Resting potential (-70 mV)"
    )

    for time in spike_times:
        ax.vlines(
            time,
            RESET_POTENTIAL,
            30,
            color="orange",
            alpha=0.7
        )

    ax.set_title(
        "Neuron Activity - Leaky Integrate-and-Fire Model"
    )
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Membrane Potential (mV)")

    ax.grid(True)
    ax.legend()

    fig.tight_layout()
    fig.savefig(GRAPH_FILE)

    return fig


# ==========================================
# ANIMATED NEURON
# ==========================================

def animate_neuron(times, spike_times):
    """Animate a neuron flashing when it fires."""

    fig, ax = plt.subplots(figsize=(11, 6))

    fig.patch.set_facecolor("#10152e")
    ax.set_facecolor("#10152e")

    ax.set_xlim(-4, 11)
    ax.set_ylim(-4, 4)
    ax.set_aspect("equal")
    ax.axis("off")

    neuron_color = "#8b7cf6"

    # Draw dendrites
    for angle in [
        1.5, 2.1, 2.7, 3.2,
        3.7, 4.2, 4.8
    ]:

        x = 2 * math.cos(angle)
        y = 2 * math.sin(angle)

        ax.plot(
            [0, x],
            [0, y],
            color=neuron_color,
            linewidth=3
        )

        for direction in [-0.5, 0.5]:

            branch_x = x + math.cos(angle + direction)
            branch_y = y + math.sin(angle + direction)

            ax.plot(
                [x, branch_x],
                [y, branch_y],
                color=neuron_color,
                linewidth=1.5
            )

    # Draw axon
    ax.plot(
        [0, 8],
        [0, 0],
        color=neuron_color,
        linewidth=6
    )

    # Draw myelin segments
    for x in [2, 3.5, 5, 6.5]:

        ax.plot(
            [x, x + 0.9],
            [0, 0],
            color="#b6adff",
            linewidth=12,
            solid_capstyle="round"
        )

    # Draw axon terminals
    for end_y in [-1.5, -0.5, 0.5, 1.5]:

        ax.plot(
            [8, 9.5],
            [0, end_y],
            color=neuron_color,
            linewidth=2
        )

    # Draw soma
    soma = Circle(
        (0, 0),
        radius=0.65,
        color=neuron_color
    )

    ax.add_patch(soma)

    # Text labels
    ax.text(
        3.5, 3,
        "NEURON ACTIVITY SIMULATION",
        color="white",
        fontsize=17,
        ha="center",
        fontweight="bold"
    )

    status = ax.text(
        3.5, 2.2,
        "",
        color="white",
        fontsize=16,
        ha="center"
    )

    time_label = ax.text(
        3.5, -2.5,
        "",
        color="white",
        fontsize=13,
        ha="center"
    )

    spike_counter = ax.text(
        3.5, -3.1,
        "",
        color="white",
        fontsize=13,
        ha="center"
    )

    spike_set = set(spike_times)
    spike_count = 0

    def update(frame):
        nonlocal spike_count

        time = times[frame]

        # Count spikes up to the current frame
        spike_count = sum(
            1 for spike in spike_times if spike <= time
        )

        if time in spike_set:

            soma.set_color("#ffcc00")

            status.set_text("ACTION POTENTIAL!")
            status.set_color("#ffcc00")

        else:

            soma.set_color(neuron_color)

            status.set_text("Resting / Integrating")
            status.set_color("white")

        time_label.set_text(
            f"Time: {time:.0f} ms"
        )

        spike_counter.set_text(
            f"Total spikes: {spike_count}"
        )

        return (
            soma,
            status,
            time_label,
            spike_counter
        )

    animation = FuncAnimation(
        fig,
        update,
        frames=len(times),
        interval=50,
        blit=False,
        repeat=True
    )

    return fig, animation


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("=== Neuron Activity Simulator ===")

    # Create stimulus data
    create_stimuli_file()

    # Load stimulus data
    currents = load_stimuli()

    # Run simulation
    times, voltages, spike_times = simulate_neuron(currents)

    # Print results
    print(f"Simulation duration: {len(times) * DT} ms")
    print(f"Number of spikes: {len(spike_times)}")
    print(f"Spike times: {spike_times}")

    # Save CSV results
    save_results(times, voltages, spike_times)

    # Create voltage graph
    graph = plot_results(
        times,
        voltages,
        spike_times
    )

    # Create animated neuron
    animation_fig, animation = animate_neuron(
        times,
        spike_times
    )

    print("Simulation completed successfully!")
    print(f"Results saved to: {RESULTS_FILE}")
    print(f"Graph saved to: {GRAPH_FILE}")

    # Display both windows
    plt.show()


if __name__ == "__main__":
    main()
