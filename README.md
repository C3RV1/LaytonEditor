# Layton Editor

Rom editor for a professor layton romhack. Created by Team Top Hat.
The instructions on how to use the editor are on the `wiki` page. You can also find there the installation instructions on the *Home* page.

Japanese is not yet supported.

Current support is limited to Professor Layton 2. Other games have not been
tested, but would probably lack many features, and stability is not guaranteed.

## Compiling

Note: LaytonEditor requires Python3 (developed under 3.9).

To install LaytonEditor, just clone the repository and install the required dependencies from the
requirements.txt file using pip install -r requirements.txt. Then, run
`python .\setup.py build_ext --inplace` to compile the cython sources.

To start the editor, run `python laytonEditor.py`.

## Thanks to...

* nwhitehead for [pyfluidsynth](https://github.com/nwhitehead/pyfluidsynth)
(modified into custom_fluidsynth)
* [https://projectpokemon.org/home/docs/mystery-dungeon-nds/dse-smdl-format-r13/](https://projectpokemon.org/home/docs/mystery-dungeon-nds/dse-smdl-format-r13/)  
* ipatix for [smd2mid](https://github.com/ipatix/smd2mid)
* vgmtrans for [vgmtrans](https://github.com/vgmtrans/vgmtrans)
* pleonex for [tinke](https://github.com/pleonex/tinke)
* Martin Korth for [gbatek](https://problemkaputt.de/gbatek.htm)
* Gericom for [MobiclipDecoder](https://github.com/Gericom/MobiclipDecoder)

## Credits

* [thatrandomstrange](https://github.com/thatrandomstranger)
* [cervi](https://github.com/C3RV1)
* [DeUloU](https://github.com/DeUloO)
