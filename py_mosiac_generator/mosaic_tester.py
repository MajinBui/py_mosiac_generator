from PIL import Image, ImageStat
import colorsys
from mosaic import *
from cluster_math import *


def main():
    option = int(input("Press 1 to make a mosiac, press 2 to normalize a picture, 0 to exit: "))
    if option is 99:
        normalize_picture("./tests/Eiffel-1.jpg", "tests_normalize/output14.png", 9)
    elif option is 0:
        exit()
    else:
        input_image_path = str(input("Input image path: "))
        output_image_path = str(input("Output image path: "))
        if option is 1:
            icon_list = generate_icon_list("../images", "png")
            generate_mosaic(input_image_path, icon_list).save(output_image_path)
        if option is 2:
            number_of_colors = int(input("Number of colors: "))
            normalize_picture(input_image_path, output_image_path, number_of_colors)

if __name__ == "__main__":
    main()
