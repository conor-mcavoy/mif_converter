# PNG to MIF converter

The purpose of this script is to take a regular PNG file and turn it into two MIFs (memory initialization files) that can be interpreted by Quartus. One of these files will contain the compressed color data, while the other will contain a color lookup-table. Togther, the two files act as a compressed version of the PNG.

For example, if the PNG uses 8 different 24-bit colors, the index file will contain each of those colors, but the data file will only store a 3-bit index for each pixel that corresponds to the location of the color in the index file. This can save a lot of space.

## Usage
You will need Python 3 and [Pillow](https://pypi.python.org/pypi/Pillow/2.7.0). Follow the instructions and you should be good to go.
On Windows:
```> python mif_converter.py input_file.png data_output_file.mif index_output_file.mif```

Feel free to make changes as you see fit.