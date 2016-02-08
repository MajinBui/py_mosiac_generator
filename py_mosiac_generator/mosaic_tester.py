from PIL import Image, ImageStat
import colorsys
from mosaic import *
from cluster_math import *

# icon_list = generate_icon_list("../images", "png")
# generate_mosaic("./tests/sfarcana.jpg", icon_list).save("output.png")

# test = Cluster([1, 1, 1], [1, 1, 1])
# print(test)

# clusterMap = ClusterMap()
# image = Image.open("../images/Aegis_of_the_Immortal.png")
normalize_picture("./tests/Eiffel-1.jpg", "./tests_normalize/output7.png", 5)
