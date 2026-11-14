"""Flask web interface for the original Day 03 neuron simulator.

Keep the original main.py and stimulus CSV files in this same folder.
"""
import os
os.environ.setdefault('MPLBACKEND', 'Agg')  # Do not launch a desktop window on web requests.

from io import StringIO
from pathlib import Path
from flask import Flask, render_template, request
from matplotlib.figure import Figure
from main import FILES, COLORS, THRESHOLD, DT, load_stimuli, simulate_neuron

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = request.form.get('pattern', 'Burst') if request.method == 'POST' else 'Burst'
    if name not in FILES:
        name = 'Burst'

    filename = FILES[name]
    if not Path(filename).is_file():
        return f'Missing stimulus file: {filename.name}', 500

    times, voltages, spikes = simulate_neuron(load_stimuli(filename))

    fig = Figure(figsize=(10, 4), facecolor='#111b31')
    ax = fig.subplots()
    ax.set_facecolor('#111b31')
    ax.tick_params(colors='#e2e8f0')
    for spine in ax.spines.values():
        spine.set_color('#64748b')
    ax.set_xlabel('Time (ms)', color='#e2e8f0')
    ax.set_ylabel('Membrane potential (mV)', color='#e2e8f0')
    ax.set_title(f'{name} neuron — membrane potential', color='white')

    # Reduce the plotted points for a lighter SVG while using ALL points for simulation.
    stride = max(1, len(times) // 1600)
    ax.plot(times[::stride], voltages[::stride], color=COLORS[name], linewidth=1.5)
    ax.axhline(THRESHOLD, color='#fb7185', linestyle='--', alpha=.85, label='Firing threshold')
    if spikes:
        ax.scatter(spikes, [THRESHOLD] * len(spikes), color='#facc15', s=16,
                   label='Spikes', zorder=4)
    ax.legend(facecolor='#1e293b', labelcolor='white')
    ax.grid(alpha=.13)
    fig.tight_layout()
    output = StringIO()
    fig.savefig(output, format='svg', facecolor=fig.get_facecolor())
    svg = output.getvalue()
    # SVG is generated entirely from numeric data by Matplotlib, not user-supplied HTML.
    return render_template('index.html', name=name, patterns=FILES.keys(),
                           graph=svg, spike_count=len(spikes),
                           duration_s=len(times) * DT / 1000,
                           first_spikes=spikes[:10])

if __name__ == '__main__':
    app.run(debug=True)
