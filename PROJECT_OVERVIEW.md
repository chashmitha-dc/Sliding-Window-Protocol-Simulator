# Sliding Window Protocol Simulator

## Overview

This project is a Python-based desktop application for visualizing and comparing sliding window protocols used in data-link and transport-layer networking. The main goal is to help students and learners understand how protocols like Stop-and-Wait, Go-Back-N, and Selective Repeat behave under different network conditions such as packet loss, acknowledgement loss, delays, and timeouts.

The current version is an early working prototype: the core simulation logic and GUI are in place, but the project is still evolving toward a more complete educational and research-oriented simulator.

## Project purpose

The simulator is designed to:

- model packet transmission under noisy network conditions
- compare how different ARQ protocols react to loss and retransmission
- show protocol behavior through a graphical user interface
- calculate performance metrics such as throughput and efficiency
- help explain sliding-window concepts in a beginner-friendly way

## Current status

The repository contains a functioning foundation for the simulator with the following major pieces implemented:

- a Tkinter-based desktop application shell
- protocol configuration controls
- simulation event logging and results display
- animated sender/receiver communication panel
- comparison window for side-by-side protocol analysis
- working protocol simulation logic for three protocol types
- performance metrics computation

The project is not yet a fully polished production app; several placeholder modules remain and some features are intentionally minimal or incomplete.

## Technology stack

- Python 3.11+
- Tkinter for the GUI
- Matplotlib for protocol comparison charts
- NumPy for numerical support and analysis
- Pillow for image support

## Application flow

The runtime flow is straightforward:

1. `main.py` launches the app.
2. `gui/main_window.py` creates the main window and control panel.
3. The user selects a protocol, configures parameters, and starts a simulation.
4. `simulation/simulator.py` routes the job to the correct protocol implementation.
5. The selected protocol runs a simulated transmission, including loss/retransmission logic.
6. Performance metrics are calculated.
7. Results are displayed in the event log and comparison panel.

## Main project structure

```text
Sliding_Window_Simulator/
├── README.md
├── main.py
├── requirements.txt
├── PROJECT_OVERVIEW.md
├── analysis/
│   ├── __init__.py
│   ├── charts.py
│   └── performance.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── gui/
│   ├── animation_panel.py
│   ├── comparison_panel.py
│   ├── input_panel.py
│   ├── main_window.py
│   └── results_panel.py
├── protocols/
│   ├── __init__.py
│   ├── go_back_n.py
│   ├── selective_repeat.py
│   └── stop_and_wait.py
├── simulation/
│   ├── __init__.py
│   ├── event_manager.py
│   ├── network.py
│   └── simulator.py
├── tests/
│   ├── __init__.py
│   └── test_protocols.py
├── reports/
└── assets/
```

## Core modules and responsibilities

### `main.py`
This is the entry point for the application. It creates the main window and runs the Tkinter event loop.

### `config/settings.py`
Contains basic application constants such as:

- application title
- window size
- default UI configuration

### `gui/main_window.py`
This is the central application window. It contains:

- protocol selection controls
- simulation parameter fields
- Start Simulation button
- Compare All Protocols button
- Reset button
- event log display
- performance results display
- status bar

It reads user input, validates it, executes the chosen simulation, and updates the UI with results.

### `gui/animation_panel.py`
A Tkinter canvas-based animation panel that visually models:

- sender and receiver endpoints
- data transmission lane
- acknowledgement lane
- packet loss indicators
- sender/receiver status updates

### `gui/comparison_panel.py`
Builds a Matplotlib bar chart comparing throughput and efficiency across protocols. This panel is used when the user chooses to compare all protocols together.

### `simulation/simulator.py`
This acts as the central dispatcher for protocol execution. It:

- validates input values
- selects the correct protocol implementation
- invokes the simulation
- calculates performance metrics
- returns structured results

### `protocols/stop_and_wait.py`
Implements the one-bit sliding window / Stop-and-Wait ARQ logic. It simulates:

- frame transmission
- packet loss
- ACK loss
- timeout handling
- retransmissions
- delivery tracking

This is a classic protocol where only one frame can be in flight at a time.

### `protocols/go_back_n.py`
Implements Go-Back-N ARQ behavior. It simulates a sliding window where:

- multiple frames can be sent before an ACK is received
- a lost packet causes retransmission of the whole window from the last successful acknowledgement
- cumulative ACKs are used

### `protocols/selective_repeat.py`
Implements Selective Repeat ARQ. It simulates:

- a sliding window with multiple outstanding frames
- independent ACK tracking for each frame
- retransmission only of unacknowledged frames
- more efficient handling than Go-Back-N when errors are sparse

### `analysis/performance.py`
Computes:

- throughput in frames per second
- transmission efficiency percentage

These are derived from simulation results and the total number of frames sent.

## Simulated parameters

The project currently allows users to configure:

- protocol type
- window size
- number of frames
- transmission delay
- ACK delay
- packet loss percentage
- ACK loss percentage
- timeout duration

This gives a practical way to explore behavior under varying network conditions.

## Simulation behavior

The project currently models the following factors:

- random packet loss
- random ACK loss
- time-based retransmission logic
- timeout waiting periods
- event logging for each major transmission stage
- cumulative metrics for total transmissions and retransmissions

The simulation emphasis is on understanding how networking protocols recover from errors and how that affects performance.

## What is already done

At this point, the project includes a solid foundation for an educational networking simulator:

- GUI skeleton and form layout
- main simulation loop and validation
- three ARQ protocol implementations
- algorithmic result generation
- comparison charts
- animation support for events
- modular code organization

## What is still incomplete or planned

The project README explicitly notes that it is still being built incrementally. Current gaps include:

- a more polished, full-featured GUI
- richer analytics and reporting
- deeper protocol comparison views
- more advanced animation and visual timeline tools
- extended testing coverage
- possible adaptability for more protocols or custom scenarios

The placeholder files in `gui/input_panel.py`, `simulation/network.py`, and `tests/test_protocols.py` suggest that some components were intended to be expanded in later versions.

## Execution

To run the application from the project root:

```bash
python main.py
```

If using a virtual environment, activate it first and install dependencies from `requirements.txt`.

## Project significance

This project is valuable as a learning tool because it turns abstract networking concepts into a concrete, interactive experience. It is especially useful for understanding:

- window-based transmission
- retransmission strategies
- timeout behavior
- reliability vs. efficiency trade-offs
- protocol choice under loss-prone networks

## Summary

The Sliding Window Protocol Simulator is an educational Python application that models the behavior of network reliability protocols in a graphical and interactive way. It currently includes a functional early-stage implementation of Stop-and-Wait, Go-Back-N, and Selective Repeat, along with a Tkinter interface, simulation engine, comparison charts, and animated event visualization.

The repository is in a promising prototype stage, with the core architecture already in place and room for further expansion into a richer, more complete simulator.
