
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

FILES = {
    "Burst": BASE_DIR / "stimuli_burst.csv",
    "Periodic": BASE_DIR / "stimuli_periodic_4s.csv",
    "Inhibited": BASE_DIR / "stimuli_inhibited.csv"
}

# ==========================================
# NEURON PARAMETERS
# ==========================================

RESTING = -70.0
THRESHOLD = -55.0
RESET = -70.0
TAU = 10.0
RESISTANCE = 1.0
DT = 1.0  # milliseconds

COLORS = {
    "Burst": "#a78bfa",
    "Periodic": "#38bdf8",
    "Inhibited": "#fb923c"
}


# ==========================================
# LOAD STIMULI
# ==========================================

def load_stimuli(filename):
    """Read current values from a CSV file."""

    currents = []

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            currents.append(float(row["current"]))

    return currents


# ==========================================
# LIF NEURON MODEL
# ==========================================

def update_voltage(voltage, current):
    """Calculate membrane voltage."""

    change = (DT / TAU) * (
        RESTING - voltage + RESISTANCE * current
    )

    return voltage + change


def simulate_neuron(currents):
    """Simulate a neuron and detect spikes."""

    voltage = RESTING

    times = []
    voltages = []
    spikes = []

    for step, current in enumerate(currents):

        time = step * DT
        voltage = update_voltage(voltage, current)

        if voltage >= THRESHOLD:
            spikes.append(time)
            voltage = RESET

        times.append(time)
        voltages.append(voltage)

    return times, voltages, spikes


# ==========================================
# SAVE RESULTS
# ==========================================

def save_results(name, times, voltages, spikes):
    """Save simulation results to CSV."""

    filename = BASE_DIR / f"results_{name.lower()}.csv"
    spike_set = set(spikes)

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["time_ms", "voltage_mv", "spike"])

        for time, voltage in zip(times, voltages):
            writer.writerow([
                time,
                round(voltage, 2),
                int(time in spike_set)
            ])


# ==========================================
# DRAW A NEURON
# ==========================================

def draw_neuron(ax, color):
    """Draw a simplified neuron."""

    ax.set_xlim(-3, 10)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")
    ax.axis("off")

    # Dendrites
    for angle in [
        1.5, 2.1, 2.7, 3.2,
        3.7, 4.2, 4.8
    ]:
        x = 1.8 * math.cos(angle)
        y = 1.8 * math.sin(angle)

        ax.plot(
            [0, x], [0, y],
            color=color, linewidth=2
        )

        for direction in [-0.5, 0.5]:
            ax.plot(
                [x, x + math.cos(angle + direction)],
                [y, y + math.sin(angle + direction)],
                color=color, linewidth=1
            )

    # Axon
    ax.plot(
        [0, 7.5], [0, 0],
        color=color, linewidth=5
    )

    # Myelin segments
    for x in [2, 3.5, 5, 6.5]:
        ax.plot(
            [x, x + 0.8], [0, 0],
            color="#c4b5fd",
            linewidth=10,
            solid_capstyle="round"
        )

    # Axon terminals
    for y in [-1.3, -0.4, 0.4, 1.3]:
        ax.plot(
            [7.5, 9], [0, y],
            color=color, linewidth=2
        )

    soma = Circle((0, 0), 0.6, color=color)
    ax.add_patch(soma)

    return soma


# ==========================================
# ANIMATION
# ==========================================

def animate_neurons(results):
    """Animate all three neurons simultaneously."""

    fig, axes = plt.subplots(
        3, 2,
        figsize=(14, 9),
        gridspec_kw={"width_ratios": [1, 1.4]}
    )

    fig.patch.set_facecolor("#10152e")

    fig.suptitle(
        "Three Neuron Activity Patterns",
        fontsize=19,
        color="white",
        fontweight="bold"
    )

    neuron_artists = {}
    graph_artists = {}

    names = list(results.keys())

    for i, name in enumerate(names):

        ax_neuron = axes[i, 0]
        ax_graph = axes[i, 1]

        ax_neuron.set_facecolor("#10152e")
        ax_graph.set_facecolor("#10152e")

        color = COLORS[name]

        soma = draw_neuron(ax_neuron, color)

        label = ax_neuron.text(
            3, 2.3,
            name.upper() + " NEURON",
            color="white",
            fontsize=13,
            ha="center"
        )

        status = ax_neuron.text(
            3, -2.3,
            "",
            color="white",
            fontsize=11,
            ha="center"
        )

        times = results[name]["times"]
        voltages = results[name]["voltages"]

        # Voltage graph
        ax_graph.plot(
            times,
            voltages,
            color=color,
            linewidth=1.2
        )

        ax_graph.axhline(
            THRESHOLD,
            color="red",
            linestyle="--",
            alpha=0.7
        )

        ax_graph.set_xlim(0, max(times))
        ax_graph.set_ylim(-85, -45)

        ax_graph.tick_params(colors="white")
        ax_graph.set_ylabel("mV", color="white")

        cursor = ax_graph.axvline(
            0,
            color="yellow",
            linewidth=2
        )

        neuron_artists[name] = (soma, status)
        graph_artists[name] = cursor

    # Use one animation frame per 20 ms
    total_steps = min(
        len(results[name]["times"]) for name in names
    )

    frames = list(range(0, total_steps, 20))

    # Precompute spike sets
    spike_sets = {
        name: set(results[name]["spikes"])
        for name in names
    }

    def update(frame):

        for name in names:

            times = results[name]["times"]
            spikes = results[name]["spikes"]

            soma, status = neuron_artists[name]
            cursor = graph_artists[name]

            time = times[frame]

            # A spike occurred during the last 20 ms
            recent_spike = any(
                (time - 20) < spike <= time
                for spike in spikes
            )

            if recent_spike:
                soma.set_color("#ffdd00")
                status.set_text("ACTION POTENTIAL!")
                status.set_color("#ffdd00")
            else:
                soma.set_color(COLORS[name])
                status.set_text("Resting / Integrating")
                status.set_color("white")

            cursor.set_xdata([time, time])

        return []

    animation = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=40,
        repeat=True,
        blit=False
    )

    plt.tight_layout()
    return fig, animation


# ==========================================
# MAIN
# ==========================================

def main():

    print("=== THREE NEURON SIMULATOR ===")

    results = {}

    for name, filename in FILES.items():

        if not filename.exists():
            print(f"Missing file: {filename}")
            return

        currents = load_stimuli(filename)

        times, voltages, spikes = simulate_neuron(currents)

        results[name] = {
            "times": times,
            "voltages": voltages,
            "spikes": spikes
        }

        save_results(name, times, voltages, spikes)

        print(f"\n{name} neuron:")
        print(f"Duration: {len(times) * DT} ms")
        print(f"Number of spikes: {len(spikes)}")
        print(f"First spike times: {spikes[:10]}")

    fig, animation = animate_neurons(results)

    print("\nSimulation completed successfully!")
    print("Close the animation window to exit.")

    plt.show()


if __name__ == "__main__":
    main()
