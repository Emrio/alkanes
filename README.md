# alkanes
> 🧪 Naming non-cyclical alkanes using the official IUPAC nomenclature

## Installation

### Requirements

This program uses `python` version 3 or higher.

### Run

1. Download the project [here](link-download)

2. Open a terminal window and navigate to the project's folder

3. Type `python3 main.py` or `python main.py` depending on your python installation

## Features

### Interactive parser

The interactive parser allows you to create and preview alkanes before naming them gradually.
Each carbon atom is associated with a unique id to which you can add more carbon atoms.
Hydrogen atoms are placed automatically.

1. Type `parse` or `parse interactive`
2. Build your molecule by gradually adding carbon atoms to the existing ones
3. Type `-1` to name the molecule

### Manual parser

The manual parser allows you to enter carbon-carbon bonds manually and doesn't show a preview of the molecule.
It is more useful for testing pre-crafted molecules.
Hydrogen atoms are placed automatically.

1. Type `parse manual`
2. Enter the number N of carbon atoms in your molecule. Carbon atoms are named with numbers from 0 to N-1
3. Enter the number L of carbon-carbon bonds
4. Enter L lines describing the molecule (e.g.: `0 5` if carbon #0 and #5 are linked)

## Configuration

The project comes with the files `multiplicative.txt` and `names.txt`.
The first contains prefixes for repeated ramifications (`dimethyl`, `triethyl`) and the second the names of ramifications (`pentyl`, `nonyl`).

You may add more prefixes and ramification names to the list for bigger molecules.

## Limitations

- Each carbon atom can have bonds with a maximum of four other atoms (sorry, this is how chemistry works)
- The default configuration can only name ramifications with up to 100 carbon atoms, and each ramification can have the same sub-ramification at most seven times.
- The interactive parser can handle at most 64 carbon atoms (there are only 64 ids). The manual parser has no such limitation
- The interactive previewer maps a 3D shape on a 2D plane. Therefore, some molecules can't be previewed. However, you can continue to build a molecule even tho it is not shown
- The interactive previewer is still a bit buggy

## Contributing

Feel free to contribute to the project!
Please follow the [guidelines][link-contribution] when contributing!

## License

This project is licensed under the [MIT License](link-license).

[link-download]: https://github.com/TheEmrio/alkanes/archive/master.zip
[link-license]: https://github.com/TheEmrio/alkanes/blob/master/LICENSE
[link-contribution]: https://github.com/TheEmrio/alkanes/blob/master/CONTRIBUTING.md
