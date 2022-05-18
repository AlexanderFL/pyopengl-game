# Game client

Developed using Python 3.9.0, pygame 2.0.1 and pyopengl version 3.1.5

## Setup
First, be located within the same file this README.md is located in
Using python virtual environments is highly recommended

- Setup venv `py -m venv game-venv` && `./game-venv/Scripts/activate`
- Install modules `python -m pip install -r requirements.txt`
- Run the game `python ./StartGame.py`

## Controls
Mouse movement to look around
'W-A-S-D' to move
'LShift' to sprint
'x' to change color of lights
'LClick' to shoot

## Configuring game
Use the 'config' file located in the working directory and modify to specific needs.

If the world sky is blue, then the game is successfully connected to a server.
If the world sky is red, then the game is not connected to any server.
