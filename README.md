# Layton Editor

Rom editor for a professor layton romhack. Created by Team Top Hat.
The instructions on how to use the editor are on the `wiki` page.

Japanese has not been tested and might not work.

## Installation

To install the LaytonEditor just clone this repository and install the
dependencies listed on `requirements.txt`.

To run just execute `python laytonEditor.py`.

There are a few features
which require additional dependencies to be executed, like synthesis
for background music.

## Enabling Background Music

The editor can work without following these instructions.

Background music requires a C library called fluidsynth which can be
downloaded from
[https://github.com/FluidSynth/fluidsynth/releases/](https://github.com/FluidSynth/fluidsynth/releases/)
for window users. For other users follow the instructions at
[https://github.com/FluidSynth/fluidsynth/wiki/Download](https://github.com/FluidSynth/fluidsynth/wiki/Download).

Then, copy the library to `./custom_fluidsynth/fluidsynth/`. If the folder
doesn't exist, create it. You also need the layton2.sf2 soundfont which is
not available to the public at the moment. If you were to have it, copy it
to `./pygame_utils/layton2.sf2`.

## Note about text fonts

You may see that the text looks different than from the original game,
and that's  because the LaytonEditor doesn't include the game text fonts.
Instead, it  includes a default font which serves the same purpose. If
you were to have  the fonts, export them to `data_permanent/fonts/`. In
future versions, the fonts will be automatically extracted from the rom.

## Thanks to...

* nwhitehead for [pyfluidsynth](https://github.com/nwhitehead/pyfluidsynth)
(modified into custom_fluidsynth)
* [https://projectpokemon.org/home/docs/mystery-dungeon-nds/dse-smdl-format-r13/](https://projectpokemon.org/home/docs/mystery-dungeon-nds/dse-smdl-format-r13/)  
* ipatix for [smd2mid](https://github.com/ipatix/smd2mid)
* vgmtrans for [vgmtrans](https://github.com/vgmtrans/vgmtrans)
* pleonex for [tinke](https://github.com/pleonex/tinke)

## Credits

* [thatrandomstrange](https://github.com/thatrandomstranger)
* [cervi](https://github.com/C3RV1)
