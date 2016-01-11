from PIL import Image, ImageStat, ImageFilter
import glob, os
import colorsys
import random
from math import sqrt, pow

ICON_SIZE_X = 32
ICON_SIZE_Y = 32

def euclidean_distance_HSV(cord_p, cord_q):
    total = 0
    for i in range(0, len(cord_p)):
        total += pow(cord_p[i]-cord_q[i], 2)
    return sqrt(total)


def generate_icon_list(folder_path, extension):
    icon_list = []
    for infile in glob.glob(folder_path+"/*."+extension):
        file, ext = os.path.splitext(infile)
        image = Image.open(infile)
        image = image.convert("RGB")
        data = {}
        data["image"] = image
        r,g,b = ImageStat.Stat(image).median
        data["rgb"] = (r,g,b)
        # data.append(colorsys.rgb_to_hsv(r, g, b))
        icon_list.append(data)
    return icon_list


def find_nearest_color(icon_list, RGB):
    # HSV_RS = colorsys.rgb_to_hsv(RGB[0], RGB[1], RGB[2])
    HSV_RS = RGB
    current_low = 0  # Lower is more similar
    current_icon = None
    for icon in icon_list:
        HSV_LS = icon["rgb"]
        temp = euclidean_distance_HSV(HSV_LS, HSV_RS)
        if (current_icon is None or current_low > temp):
            current_low = temp
            current_icon = icon
    return current_icon

def resize_icon_list(icon_list, size):
    for icon in icon_list:
        icon_w,icon_h = icon["image"].size
        new_w,new_h = size

        if (icon_w != new_w):
            icon["image"] = icon["image"].resize((new_w,int(new_w*icon_h/icon_w)))
            icon_w,icon_h = icon["image"].size

        if (new_h != icon_h):
            left = 0
            right = left + new_w
            upper = int((icon_h - new_h)/2)
            lower = upper + new_h

            icon["image"] = icon["image"].crop((left,upper,right,lower))
            icon_w,icon_h = icon["image"].size
    return icon_list


def generate_mosaic(original_image_path, icon_list):
    original_image = Image.open(original_image_path)
    mosaic_image = Image.new("RGB", (original_image.width*ICON_SIZE_X, original_image.width*ICON_SIZE_Y))

    icon_list = resize_icon_list(icon_list,(ICON_SIZE_X,ICON_SIZE_Y))

    for w in range(0, original_image.width):
        for h in range(0, original_image.height):
            original_pixel_rgb = original_image.getpixel((w,h))
            icon = find_nearest_color(icon_list, original_pixel_rgb)

            mosaic_image.paste(icon["image"],(w*ICON_SIZE_X,h*ICON_SIZE_X))

    return mosaic_image
