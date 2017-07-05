# HarnessGUI

## Project Summary
Python GUI built in Tkinter for operating the Harness with ease. The Harness serves as the "gate-keeper" of the MPS, operating between MME and Pleniter. See **MME Gitlab documentation** for more info on the Harness set-up.

## Prerequisites
The following are needed to run the Harness GUI software
- Python2 (2.7.5 and above)
- Tkinter library for GUI features

## Main Features
- Harness is run from a single-click (logger, planning server, Harness compiled+run)
- GUI Integrated w/ Harness (Server-side VM)
- Error checks for shell scripts on the Status Check window
- Configuration settings editable for user

## Running the Code
To run the code, clone this repo onto Pleniter subnet. Then, from inside the HarnessGUI directory: 
```python
python main.py
```

## What's Ahead
- Implement Start Planning option
- Implement a more robust check-pointing scheme
- Implement more robust shell scripting in back-end
- Improve UI as need be, document code for others
- Export to exe, stand-alone application for end user

## Authors
- **Justin Alvey** - initial work, developed during internship

## Acknowledgements
- **JP Chavez**, OneWeb
- **Zach Meza**, Oneweb
