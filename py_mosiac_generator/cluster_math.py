from PIL import Image, ImageStat, ImageColor
from math import sqrt, pow

def euclidean_distance(coord_p, coord_q):
    total = 0
    for i in range(0, len(coord_p)):
        total += pow(coord_p[i]-coord_q[i], 2)
    return sqrt(total)

def find_nearest_coord(coord_list, coord_rhs):
    current_low = 0  # Lower is more similar
    current_coord = None
    for coord in coord_list:
        coord_lhs = coord
        temp = euclidean_distance(coord_lhs, coord_rhs)
        if (current_coord is None or current_low > temp):
            current_low = temp
            current_coord = coord
    return current_coord

def print_loading_bar(current, denominator, num_of_hashtags):
    temp_string = ""
    for i in range(0, num_of_hashtags):
        if (i < int(current/denominator * num_of_hashtags)):
            temp_string = temp_string + "#"
        else:
            temp_string += " "
    output_string = "[{0}]".format(temp_string)
    if current < denominator:
        print(output_string + " " + str(int(current/denominator * 100)) + "%", end='\r')
    else:
        print(output_string + " " + str(int(current/denominator * 100)) + "%", end='\n')

class Cluster:


    def __init__(self, lowercoord = [0, 0, 0], uppercoord = [0, 0, 0]):
        self.plots = []
        self.lowercoord = [0, 0, 0]
        self.uppercoord = [0, 0, 0]
        self.average_coord = [0, 0, 0]
        if (isinstance(lowercoord, list)):
            self.lowercoord = lowercoord
        if (isinstance(uppercoord, list)):
            self.uppercoord = uppercoord

    def plot(self, coord, count):
        if ((coord[0] >= self.lowercoord[0] and coord[1] >= self.lowercoord[1] and coord[2] >= self.lowercoord[2]) and
            (coord[0] < self.uppercoord[0] and coord[1] < self.uppercoord[1] and coord[2] < self.uppercoord[2])):
            for i in range(count):
                self.plots.append(coord)
            return True

    def purge(self, coord):
        if ((coord[0] >= self.lowercoord[0] and coord[1] >= self.lowercoord[1] and coord[2] >= self.lowercoord[2]) and
            (coord[0] < self.uppercoord[0] and coord[1] < self.uppercoord[1] and coord[2] < self.uppercoord[2])):
            plots = []

    def average_color(self):
        if (len(self.plots) > 0):
            for plot in self.plots:
                self.average_coord[0] = self.average_coord[0] + plot[0]
                self.average_coord[1] = self.average_coord[1] + plot[1]
                self.average_coord[2] = self.average_coord[2] + plot[2]
            self.average_coord[0] = int(self.average_coord[0]/len(self.plots))
            self.average_coord[1] = int(self.average_coord[1]/len(self.plots))
            self.average_coord[2] = int(self.average_coord[2]/len(self.plots))


    def __str__(self):
        string = "Number of plots: {0} Upper Coordinate: {1} Lower Coordinate: {2}".format(len(self.plots), self.uppercoord, self.lowercoord)
        return string


class ClusterMap:
    """
        Creates a list of clusters that holds coordinates that are located within
        its boundaries
    """
    def __init__(self, x=255 , y=255 , z=255, size=20):
        """"
            Initializes the map.
            :param x the length of the x axis
            :param y the length of the y axis
            :param z the length of the z axis
            :size the size of each cluster
        """
        self.size = size
        self.cluster_list = []
        for i in range(0, x, size):
            for j in range(0, y, size):
                for k in range(0, z, size):
                    self.cluster_list.append(Cluster([i, j, k], [i+20, j+20, k+20]))

    def purge(self, coord):
        """
            Clears a cluster of the data it holds
            :param coord the coordinate of the cluster to be reset
        """
        for cluster in self.cluster_list:
            cluster.purge(coord)

    def plot(self, coord, count):
        """
            Searches through the cluster list and plots the coordinate if a
            cluster is found.
            :param coord the coordinate to plot
            :param count the number of times to plot the coord
        """
        for cluster in self.cluster_list:
            cluster.plot(coord, count)

    def average_colors(self):
        """
            Sets the average coordinate for each cluster
        """
        for cluster in self.cluster_list:
            cluster.average_color()

def normalize_picture(input_image_path, output_image_path, num_of_colors):
    """
        Reduces the amount of colors a picture has has.
        :param input_image_path the path input file
        :param output_image_path the output file path
        :param num_of_colors the number of colors to reduce the image to
    """
    print("Loading files...")
    input_image = Image.open(input_image_path)
    output_image = Image.new("RGB", (input_image.width, input_image.height))
    clusterMap = ClusterMap(size=int(255/num_of_colors))
    pixel_count = input_image.width *input_image.height
    print("Analyzing image...")
    count = 0
    for color in input_image.getcolors(maxcolors=1000000):
        clusterMap.plot(list(color[1]), color[0])
        count = count + color[0]
        print_loading_bar(count, pixel_count, 20)

    clusterMap.average_colors()

    plotted_points = [cluster for cluster in clusterMap.cluster_list if len(cluster.plots) > 0]
    plotted_points = sorted(plotted_points, key=lambda x: len(x.plots), reverse=True)[:num_of_colors]
    color_list = [cluster.average_coord for cluster in plotted_points]
    count = 0
    print("Recreating image...")
    for w in range(0, output_image.width):
        for h in range(0, output_image.height):
            input_pixel_rgb = input_image.getpixel((w,h))
            color = find_nearest_coord(color_list, input_pixel_rgb)
            temp = Image.new("RGB", (1,1), tuple(color))
            output_image.paste(temp, box=(w,h))
            count = count + 1
            print_loading_bar(count, pixel_count, 20)
    output_image.save(output_image_path)
