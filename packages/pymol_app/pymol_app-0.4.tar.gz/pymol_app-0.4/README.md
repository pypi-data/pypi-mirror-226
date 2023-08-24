# pymol
De Mol Eliminatie App (mac only)

# Installation

## Python

Make sure [python](https://www.python.org/downloads/) is installed on your system

## pip

Make sure pip is installed:

open Terminal

```python -m ensurepip --upgrade```

## pymol_app

Use pip to install pymol:

```pip install pymol_app```

To confirm `pymol` works, try:

```pymol```

# Usage

Open your favourite text editor and type something like this:

```
player1,green
player2,green
player3,red
player4,green
```

Save it with the `.csv` extention (i.e., as `eliminatie.csv`) anywhere on your computer

In the Terminal, pass the path of that file to `pymol` like this:

```pymol [path to directory]/eliminatie.csv```

Tips:
- You can navigate your terminal to the folder where `eliminatie.csv` is located (by using `cd`). 
- Or, you can drag the file from the finder to the Terminal to copy the whole path (I find this the easiest).
- Using the up arrow key, you can select previously run commands

The app should start full screen (quit by pressing ESC)

simply type names and press enter to reveal the screen

Have fun!
