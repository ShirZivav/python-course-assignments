# Day 04 – Neuron Activity Simulator Web App

## Project Description

This project extends my Day 03 Python neuron simulator into an interactive web application using Flask.

The application uses the Leaky Integrate-and-Fire (LIF) model to simulate how neurons respond to electrical stimulation.

Users can select between three neuronal activity patterns:

- **Burst:** Multiple spikes occurring in short bursts.
- **Periodic:** Spikes occurring approximately every four seconds.
- **Inhibited:** Reduced neuronal activity due to inhibitory stimulation.

The web application displays a graph of the neuron's membrane potential and the number of spikes detected.

## Reusing the Day 03 Project

The Flask application imports the original `load_stimuli()` and `simulate_neuron()` functions from `main.py`.

This allows the web application to reuse the same scientific calculations and parameters as the original Python simulator.

The original `day03` folder remains unchanged.

## Project Files

- `main.py` – Original neuron simulation and animation.
- `app.py` – Flask web application.
- `templates/index.html` – Web page interface.
- `static/style.css` – Website styling.
- `stimuli_burst.csv` – Burst stimulus data.
- `stimuli_periodic_4s.csv` – Periodic stimulus data.
- `stimuli_inhibited.csv` – Inhibitory stimulus data.
- `requirements.txt` – Python dependencies.

## Technologies Used

- Python
- Flask
- Matplotlib
- HTML and CSS
- CSV files

## Installation

Open a terminal inside the `day04` folder and install the required libraries:

```bash
python -m pip install -r requirements.txt
```

## Running the Web Application

Run:

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

Select Burst, Periodic, or Inhibited and click **Run Simulation**.

## Running the Original Simulator

Run:

```bash
python main.py
```

The original Matplotlib animation will open.

## Testing

The following tests were completed successfully:

- The original Day 03 neuron simulator runs and displays the Matplotlib animation.
- The Flask web server starts successfully.
- All three neuronal activity patterns (Burst, Periodic, and Inhibited) run successfully in the web application.
- Each simulation displays a membrane potential graph and spike count.
- The original Day 03 project remains intact.

## AI Assistance

ChatGPT was used to help adapt the original Python simulator into a Flask web application, reuse existing simulation functions, troubleshoot errors, and prepare documentation.

Prompts used during development included:

1. "Help me turn my Day 03 neuron simulator into a Flask web application."
2. "Reuse the existing simulation functions from main.py."
3. "Create a web interface for selecting different neuronal activity patterns."
4. "Help me fix the ModuleNotFoundError when running app.py."
5. "Explain how to run and test both the original Python program and the Flask application."

## Conclusion

This project demonstrates how an existing scientific Python program can be extended into a web application while preserving its original computational logic.