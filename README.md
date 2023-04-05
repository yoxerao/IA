## How to run
* Verify that you have pip installed by running `pip -V`
* In the project root foler, run `pip install -r requirements.txt`
* Now you can simply run `python main.py` in the root folder and use the graphical interface to interact with the program. Note that a lot of complementary information will only show on the terminal.

## Notes on use:
* Pressing 'Main Menu' while in an algorithm menu will reset the shared random solution, simply use the same main menu when comparing algorithms
* When changing the amount of establishments it is imperative that the main menu is reset if an algorithm menu has been opened before with a different amount of establishments. You can reset the menu by pressing the main menu button in any algorithm menu.

## Known bugs:
* GA gets stuck in particular situations, when the number of establishments is low.