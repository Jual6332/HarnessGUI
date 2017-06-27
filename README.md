# HarnessGUI

## Project Summary
Python GUI built in Tkinter for operating the Harness with ease. The Harness serves as the "gate-keeper" of the MPS, operating between MME and Pleniter. See **MME Gitlab documentation** for more info on the Harness set-up.

## Prerequisites
The following are needed to run the Harness GUI software
- Python3 (3.3 or newer required, developed on 3.5.2)
- Tkinter library for GUI features

## Main Features
- Error checks for shell scripts on the Status Check window
- Java Project for Harness is run from GUI (via shell)
- Configuration settings editable for user
- Configuration settings loaded automatically

## Running the Code
To run the code, clone this repo. Then, from inside the HarnessGUI directory: 
```python
python3 main.py
```

## What's Ahead
- Integrate GUI w/ Harness for testing
- Implement a more robust shell scripting in back-end
- Make changes to UI as need be, document code for others

## Authors
- **Justin Alvey** - initial work, completed during internship

## Acknowledgements
- **JP Chavez**, OneWeb
- **Zach Meza**, Oneweb
