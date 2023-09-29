# Inkbound Damage
This project creates a damage tracker for the [Inkbound](https://store.steampowered.com/app/1062810/Inkbound/) game created by Shiny Shoe.

This tracker was created on a whim and is in no way production code.  No testing has been done and in no way should this project be considered complete.  Use at your own risk and understand that bugs are likely.

For those reviewing the source code I apologize for how atrocious it is :) I do not have experience with Python and this project is a learning experience for me.  Feel free to suggest improvements!

![Example](/images/example.png)

### Functionality
This project currently tracks all damage events in the logs found at `%USERPROFILE%\AppData\LocalLow\Shiny Shoe\Inkbound\`
and parses them to display damage breakdowns by ability and player within a game of Inkbound.

This window is set to appear on top of all other windows, so it can be viewed while in fullscreen while playing.

The is parsed in real time by a separate thread to allow for the damage numbers to be updated and displayed in real time.

The parser will reset display each time a new run is started in game.

NOTE: The logs are overwritten by Inkbound each time the game is launched, currently there is no way to persist runs between game launches and you will likely run into weird behaviours if you resume a run.

![Example](/images/example_video.gif)

Data is displayed in sections for each character in the run.  Character steam name, class, and % of total damage is displayed in the header.

Underneath each header total damage dealt and received is displayed.  Bellow that damage broken down by damage source is displayed in descending order.  Percentage of total damage dealt for that player by that ability is also displayed.

### Running the Tracker
Source code is available for review, see `InkboundDamage.py` for running the application.

For convenience an exe is included in `./dist/InkboundDamage` NOTE: Windows does not like this python executable and will likely warn you that it is a virus.  I can't be bothered to figure out why this is so if you are at all concerned about allowing the execution of it DO NOT grant permission.  Instead review source code and run through `InkboundDamage.py`

There are probably hoops you need to jump through to run from source code but I'm not sure what they are.  If you run into them feel free to reach out, if you solve them also feel free to reach out and I can add to the README.

### Creating an Executable
The executable included in `./dist/InkboundDamage` is created using the bellow command:
`pyinstaller --paths=venv\Lib\site-packages  src/InkboundDamage.py`

A single file executable can be created by adding the `-F` flag

### Future Work
1. Add ability to track damage across session, run, and individual combat
2. Tracking of applied status effects is already hooked up, figure out a way to display in a meaningful way
3. Add ways to persist logs / game data (Maybe an export button?)
4. Improve overall appearance
5. Add mapping of log derived names to human-readable / UI derived names
6. Figure out how to track home much damage is blocked and add tracking
7. Track which bindings, vestiges, and font of wisdom choices are made
8. Maybe add drilling into which enemies are damages, and which enemies damaged you
9. TBD

### Contact
Discord:

![](/images/discord.png)