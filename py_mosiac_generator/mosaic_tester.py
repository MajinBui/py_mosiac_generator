from PIL import Image, ImageStat
import colorsys
from mosaic import *

icon_list = generate_icon_list("../images", "png")

generate_mosaic("../sfarcana.jpg", icon_list).save("output.png")
