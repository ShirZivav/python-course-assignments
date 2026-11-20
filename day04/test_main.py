
import pytest

from main import (
    RESTING,
    RESET,
    DT,
    load_stimuli,
    update_voltage,
    simulate_neuron
)


# ==========================================
# TEST CSV LOADING
# ==========================================

def test_load_stimuli(tmp_path):
    file = tmp_path / "test_stimuli.csv"
    file.write_text("current\n10\n20.5\n-5\n")

    currents = load_stimuli(file)

    assert currents == [10.0, 20.5, -5.0]


# ==========================================
# TEST MEMBRANE VOLTAGE
# ==========================================

def test_resting_voltage():
    voltage = update_voltage(RESTING, 0)

    assert voltage == pytest.approx(RESTING)


def test_positive_current():
    voltage = update_voltage(RESTING, 10)

    assert voltage == pytest.approx(-69.0)


def test_negative_current():
    voltage = update_voltage(RESTING, -10)

    assert voltage == pytest.approx(-71.0)


def test_voltage_leak():
    voltage = update_voltage(-60.0, 0)

    assert voltage == pytest.approx(-61.0)


# ==========================================
# TEST NEURON SIMULATION
# ==========================================

def test_no_spikes_without_current():
    currents = [0.0] * 100

    times, voltages, spikes = simulate_neuron(currents)

    assert spikes == []
    assert voltages == pytest.approx([RESTING] * 100)


def test_spike_and_reset():
    currents = [0.0, 150.0]

    times, voltages, spikes = simulate_neuron(currents)

    assert spikes == [DT]
    assert voltages[-1] == pytest.approx(RESET)


def test_simulation_output_length():
    currents = [10.0, 20.0, 30.0, 40.0]

    times, voltages, spikes = simulate_neuron(currents)

    assert len(times) == len(currents)
    assert len(voltages) == len(currents)
    assert times == [0, DT, 2 * DT, 3 * DT]
