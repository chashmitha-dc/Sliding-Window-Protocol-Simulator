# Sliding Window Protocol Simulator

A beginner-friendly, interactive GUI project for exploring sliding window
protocols used in computer networks. The project is being built incrementally;
the protocol simulations and full graphical interface are not implemented yet.

## Features

- Planned simulation of One-Bit Sliding Window (Stop-and-Wait), Go-Back-N ARQ,
  and Selective Repeat ARQ.
- Planned interactive controls, animation, results, and protocol comparison.
- Modular separation of protocols, simulation, GUI, and performance analysis.

## Technology stack

- Python 3.11 or later
- Tkinter for the desktop interface (included with Windows Python when Tcl/Tk
  and IDLE are selected)
- Matplotlib and NumPy for charts and analysis
- Pillow for image support

## Installation

In Windows PowerShell, from the project directory:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Check that Tkinter is available:

```powershell
python -m tkinter
```

This should open a small Tkinter demo window. Tkinter is part of the standard
library and must not be installed with pip. If it is unavailable, modify your
Windows Python installation and enable **tcl/tk and IDLE**.

## Run the application

With the virtual environment activated:

```powershell
python main.py
```

The current application window is an initial template; protocol behavior and
the complete GUI will be added in later development steps.
