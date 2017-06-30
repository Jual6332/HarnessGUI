# HarnessGUI

## Project Summary
Python GUI built in Tkinter for operating the Harness with ease. The Harness serves as the "gate-keeper" of the MPS, operating between MME and Pleniter. See **MME Gitlab documentation** for more info on the Harness set-up.

## Prerequisites
The following are needed to run the Harness GUI software
- Python2 (2.7.5 and above)
- Tkinter library for GUI features

## Main Features
- Harness is run from a single-click (logger, planner, compiled, run)
- GUI Integrated w/ Harness
- Error checks for shell scripts on the Status Check window
- Java Project for Harness is run from GUI (via shell)
- Configuration settings editable for user

## Running the Code
To run the code, clone this repo onto Pleniter subnet. Then, from inside the HarnessGUI directory: 
```python
python main.py
```

## What's Ahead
- Implement more robust shell scripting in back-end
- Improved error checks on the Status Check window (logger running, database polled, etc)
- Make changes to UI as need be, document code for others

## Authors
- **Justin Alvey** - initial work, completed during internship

## Acknowledgements
- **JP Chavez**, OneWeb
- **Zach Meza**, Oneweb
