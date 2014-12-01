from PIL import Image, ImageDraw
import subprocess
import os
import shutil
import math
import compress

def convertJxrToPNG(path):

    print path
    outfile = "tmp.bmp"
    command = "./JxrDecApp -i " + path + " -o " + outfile

    status = subprocess.call(command.split(), shell=False)

    im = Image.open(outfile)
    im.save(path.replace(".jxr", ".png"))

    return outfile




dstFolder="/home/tbergmueller/dev/mm/databases_compressed/iitd/"

methods=['jxr']
qp=[70,75,80,100]
crs=[15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]

for m in methods:

    for crt in crs:
        singleFolderName = dstFolder + "/method_" + m + "/single/cr" + str(crt)+ "/"

        for f in os.listdir(singleFolderName):
            if not f.endswith(".jxr"):
                continue

            singleFile = singleFolderName + "/" + f

            convertJxrToPNG(singleFile)

            for q in qp:

                outFile = dstFolder + "/method_" + m + "/double/cr" + str(crt) + "/quality" + str(q) + "/" + f
                convertJxrToPNG(outFile)

                #print outFile
