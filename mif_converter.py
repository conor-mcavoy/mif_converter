import sys

from PIL import Image # you'll need to get Pillow
                      # https://pypi.org/project/Pillow/2.7.0/


header = """DEPTH = {};
WIDTH = {};
ADDRESS_RADIX = HEX;
DATA_RADIX = HEX;
CONTENT BEGIN\n"""
# required header for MIF files
# we will insert depth and width on the fly

if (len(sys.argv) > 3):
    # needs 3 args: input file, data output file, index output file
    # make sure output files end in .mif
    input_filename = sys.argv[1]
    output_data_filename = sys.argv[2]
    output_index_filename = sys.argv[3]

    image = Image.open(input_filename)

    data_file = open(output_data_filename, 'w');

    print("Image size: {}".format(image.size))
    width = image.size[0]
    height = image.size[1]

    print("Writing to data file: " + output_data_filename)

    index = 0
    all_colors = []

    data_file_str = ""
    
    for y in range(height):
        for x in range(width):
            red = image.getpixel((x,y))[0]
            green = image.getpixel((x,y))[1]
            blue = image.getpixel((x,y))[2]
            # get RGB value of pixel

            hex_value = hex(blue << 16 | green << 8 | red)
            # turns the RGB values into a hex number by bit shifting
            if hex_value not in all_colors:
                all_colors.append(hex_value)
            # only record new colors in the index file to save space

            color_index = hex(all_colors.index(hex_value))

            data_file_str += hex(index)[2:] + ":\t" + color_index[2:] + ";\n"
            index += 1

    data_width = len(all_colors).bit_length()
    # this represents the size of an index in bits
    # so the length of the index MIF will be 2^data_width

    # depth must be size of the image
    # width comes from above
    data_file.write(header.format(width*height, data_width))
    data_file.write(data_file_str + "END;")
    
    data_file.close()

    index_file = open(output_index_filename, 'w')
    
    print("Writing to index file: " + output_index_filename)

    # depth is calculated as mentioned above
    # width is automatically 24 because each color is 24 bits
    index_file.write(header.format(2**data_width, 24))
    for index, color in enumerate(all_colors):
        index_file.write(hex(index)[2:] + ":\t" + color[2:] + ";\n")

    # Quartus requires the index MIF to go to a power of 2 minus 1
    # for example the file can't end at 25, it has to go to 31
    # but we can fill it out with 0s
    while index < 2**data_width-1:
        index += 1
        index_file.write(hex(index)[2:] + ":\t" + "0;\n")
        
        
    index_file.write("END;")
    index_file.close()
    print("Done")
