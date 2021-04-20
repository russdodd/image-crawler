from PIL import Image
import PIL
import csv
import os
import pathlib
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if val != "GPSLatitude" and val != "GPSLongitude":
                    continue
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


with open('geo_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['path', 'GPSLatitude', 'GPSLongitude']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # directory to start from
    rootDir = str(pathlib.Path().absolute())
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            try:
                print('\t%s' % fname)
                exif_data = get_exif(dirName + "/" + fname)
                geo_data = get_geotagging(exif_data)
                geo_data["path"] = dirName + "/" + fname
                print(geo_data)
                writer.writerow(geo_data)

            except PIL.UnidentifiedImageError:
                print("Oops!  That was no valid image.  Try again...")
            except Exception as e:
                print(e)
