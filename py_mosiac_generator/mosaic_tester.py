from PIL import Image, ImageStat
import colorsys
from mosaic import *
from cluster_math import *

# icon_list = generate_icon_list("../images", "png")

def main():
    option = int(input("Press 1 to make a mosiac, press 2 to normalize a picture, 0 to exit: "))
    input_image_path = str(input("Input image path: "))
    output_image_path = str(input("Output image path: "))

    if option is 1:
        generate_mosaic(input_image_path, icon_list).save(output_image_path)
    if option is 2:
        number_of_colors = int(input("Number of colors: "))
        normalize_picture(input_image_path, output_image_path, number_of_colors)
    if option is 99:
        normalize_picture("./tests/sfarcana.jpg", "tests_normalize/output9.png", 5)

if __name__ == "__main__":
    main()
