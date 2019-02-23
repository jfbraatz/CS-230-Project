import os
import subprocess
import xml.etree.ElementTree as et

image_dir = "50ImagesSet1"
truth_dir = "GroundTruth50ImagesSet1"

filenames = [name.split('.')[0] for name in os.listdir(image_dir)]
for name in filenames:
    out = subprocess.getoutput("tesseract '%s/%s.png' stdout -l ara --psm 7" % (image_dir, name)).split()[-1]
    ground_truth = et.parse(truth_dir + '/' + name + '.xml').findall('content')[0].get('transcription')
    print("%s.\t Tess: %s\tTruth: %s\tEqual: %s" % (name.split('_')[-1],out, ground_truth, out == ground_truth))
