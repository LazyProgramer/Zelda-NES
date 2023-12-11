# Zelda-NES
Introduction

This repository is about the recreation of the Legend Of Zelda from NES.
Our game isn't entirely complete like the original. There's only one enemy and the map is limited to certain areas but it was redone and the code refactored.

The patterns we used were:
###  Command -> input_handler.py; command.py; commandpad.py
###  Observer -> observer.py
###  Prototype -> enemies.py; projectiles.py
###  State -> state_machine.py; state.py
###  Event Queue -> main.py
###  Component -> display_loader.py; player_sprite.py
###  Inheritance -> actors.py; enemies.py
###  Service locator -> enemy_spawner.py
###  Finite state machine -> state_machine.py; state.py
###  Broad Phase-Axis-Aligned Bounding Box -> observer.py

We implemented the Command pattern to get the action to be done by the event created (Event Queue). The event is created based on the key that was pressed and for that we use an input handler.


We created transition states so we can pass from one state to another and using the finite state machine we update the action needed.

The player and enemies inherit from the actors because there's certain things that both use and this way are not repeated.


To play the game, download the files and run main.py.