import os
import numpy as np
import xml.etree.ElementTree as et
import cv2
from shutil import copyfile


class DataProvider():
    def __init__(self, filenames, img_dir, truth_dir):
        self.filenames = filenames
        self.img_dir = img_dir
        self.truth_dir = truth_dir
        self.idx = 0

    def hasNext(self):
        "are there still samples to process?"
        return self.idx < len(self.filenames)

    def getNext(self):
        img_loc = '%s/%s.png' % (self.img_dir, self.filenames[self.idx])
        truth_loc = '%s/%s.xml' % (self.truth_dir, self.filenames[self.idx])
        word = et.parse(truth_loc).findall('content')[0].get('transcription')
        self.idx += 1
        return word, img_loc

def createIAMCompatibleDataset(dataProvider):
    "this function converts the passed dataset to an IAM compatible dataset"

    # create files and directories
    f = open('words.txt', 'w+')
    if not os.path.exists('words'):
        os.makedirs('words')

    # go through data and convert it to IAM format
    ctr = 0
    while dataProvider.hasNext():
        word, img_filename = dataProvider.getNext()
        new_filename = 'words/%d-%s.png' % (ctr, word)
        file_title = new_filename[6:-4]

        # write filename, dummy-values and text
        line = file_title + ' X X X X X X X ' + word + '\n'
        f.write(line)

        copyfile(img_filename, new_filename)

        ctr += 1

if __name__ == '__main__':
    image_dir = "APTI/Andalus/Andalus_10_Plain/set1"
    truth_dir = "APTI/XMLAndalus/XMLAndalus_10_Plain/set1"
    filenames = [name.split('.')[0] for name in os.listdir(image_dir)]
    dataProvider = DataProvider(filenames, image_dir, truth_dir)
    createIAMCompatibleDataset(dataProvider)
