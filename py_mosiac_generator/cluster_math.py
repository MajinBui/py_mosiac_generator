from PIL import Image, ImageStat, ImageColor
from math import sqrt, pow

def euclidean_distance(cord_p, cord_q):
    total = 0
    for i in range(0, len(cord_p)):
        total += pow(cord_p[i]-cord_q[i], 2)
    return sqrt(total)

def find_nearest_cord(cord_list, cord_rhs):
    current_low = 0  # Lower is more similar
    current_cord = None
    for cord in cord_list:
        cord_lhs = cord
        temp = euclidean_distance(cord_lhs, cord_rhs)
        if (current_cord is None or current_low > temp):
            current_low = temp
            current_cord = cord
    return current_cord

class Cluster:


    def __init__(self, lowerCord = [0, 0, 0], upperCord = [0, 0, 0]):
        self.plots = []
        self.lowerCord = [0, 0, 0]
        self.upperCord = [0, 0, 0]
        self.average_cord = [0, 0, 0]
        if (isinstance(lowerCord, list)):
            self.lowerCord = lowerCord
        if (isinstance(upperCord, list)):
            self.upperCord = upperCord

    def plot(self, cord):
        if ((cord[0] >= self.lowerCord[0] and cord[1] >= self.lowerCord[1] and cord[2] >= self.lowerCord[2]) and
            (cord[0] < self.upperCord[0] and cord[1] < self.upperCord[1] and cord[2] < self.upperCord[2])):
            self.plots.append(cord)
            return True

    def purge(self, cord):
        if ((cord[0] >= self.lowerCord[0] and cord[1] >= self.lowerCord[1] and cord[2] >= self.lowerCord[2]) and
            (cord[0] < self.upperCord[0] and cord[1] < self.upperCord[1] and cord[2] < self.upperCord[2])):
            plots = []

    def average_color(self):
        if (len(self.plots) > 0):
            for plot in self.plots:
                self.average_cord[0] = self.average_cord[0] + plot[0]
                self.average_cord[1] = self.average_cord[1] + plot[1]
                self.average_cord[2] = self.average_cord[2] + plot[2]
            self.average_cord[0] = int(self.average_cord[0]/len(self.plots))
            self.average_cord[1] = int(self.average_cord[1]/len(self.plots))
            self.average_cord[2] = int(self.average_cord[2]/len(self.plots))


    def __str__(self):
        string = "Number of plots: {0} Upper Coordinate: {1} Lower Coordinate: {2}".format(len(self.plots), self.upperCord, self.lowerCord)
        return string


class ClusterMap:

    def __init__(self, x=255 , y=255 , z=255, size=20):
        self.size = size
        self.cluster_list = []
        for i in range(0, x, size):
            for j in range(0, y, size):
                for k in range(0, z, size):
                    self.cluster_list.append(Cluster([i, j, k], [i+20, j+20, k+20]))

    def purge(self, cord):
        for cluster in self.cluster_list:
            cluster.purge(cord)

    def plot(self, cord):
        for cluster in self.cluster_list:
            cluster.plot(cord)

    def average_colors(self):
        for cluster in self.cluster_list:
            cluster.average_color()

def normalize_picture(input_image_path, output_image_path, num_of_colors):
    print("Loading files...")
    input_image = Image.open(input_image_path)
    output_image = Image.new("RGB", (input_image.width, input_image.height))
    clusterMap = ClusterMap(size=int(255/num_of_colors))
    pixel_count = input_image.width *input_image.height
    print("Analyzing image...")
    count = 0
    for color in input_image.getcolors(maxcolors=1000000):
        temp_string = ""
        for i in range(0, 20):
            if (i < int(count/pixel_count * 20)):
                temp_string = temp_string + "#"
            else:
                temp_string += " "
        output_string = "[{0}]".format(temp_string)
        print(output_string + " " + str(int(count/pixel_count * 100)) + "%", end='\r')
        clusterMap.plot(list(color[1]))
        count = count + 1
    print("[####################]100%")
    # clusterMap.purge([0, 0, 0])
    # clusterMap.purge([255, 255, 255])

    clusterMap.average_colors()

    plotted_points = [cluster for cluster in clusterMap.cluster_list if len(cluster.plots) > 0]
    plotted_points = sorted(plotted_points, key=lambda x: len(x.plots), reverse=True)[:num_of_colors]
    color_list = [cluster.average_cord for cluster in plotted_points]
    count = 0
    print("Recreating image...")
    for w in range(0, output_image.width):
        for h in range(0, output_image.height):
            temp_string = ""
            for i in range(0, 20):
                if (i < int(count/pixel_count * 20)):
                    temp_string = temp_string + "#"
                else:
                    temp_string += " "
            output_string = "[{0}]".format(temp_string)
            print(output_string + " " + str(int(count/pixel_count * 100)) + "%", end='\r')
            input_pixel_rgb = input_image.getpixel((w,h))
            color = find_nearest_cord(color_list, input_pixel_rgb)
            temp = Image.new("RGB", (1,1), tuple(color))
            output_image.paste(temp, box=(w,h))
            count = count + 1
    print("[####################]100%")
    output_image.save(output_image_path)
