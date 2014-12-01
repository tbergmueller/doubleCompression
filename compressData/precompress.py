from PIL import Image, ImageDraw
import subprocess
import os
import shutil
import math
import compress

def precompress(srcFolder, dstFolder, quals):
    # list files in directory
    files=os.listdir(srcFolder)

    for q in quals:
        print "Precompressing for quality " + str(q)
        folder=dstFolder + "/quality" + str(q) + "/"
        compress.mkdir_p(folder)
        for f in files:
            if not f.endswith(".bmp"):
                continue

            compress.saveAsJPG(srcFolder + "/" + f, folder + f, q)


def actuallyFind(srcFile, maxSize, method, minQ, maxQ):
    if method == 'jpg':
        tmpFile = "tmp.jpg"

        qprobe = int(math.ceil((minQ + maxQ) / 2.0))

        if qprobe == minQ or qprobe == maxQ:
            return qprobe # optimal parameter
       # print qprobe
        compress.saveAsJPG(srcFile, tmpFile, qprobe)
        curSize = os.path.getsize(tmpFile)

        if curSize < maxSize:
           return actuallyFind(srcFile,maxSize,method,qprobe,maxQ)
        else:
            return actuallyFind(srcFile,maxSize,method,minQ,qprobe)

    if method == 'jxr' or method == "jp2":
        tmpFile = "tmp." + method
        qprobe = int(math.ceil((minQ + maxQ) / 2.0))

        if (maxQ - minQ) <= 1:                              # termination condition
            curSize = os.path.getsize(tmpFile)

            while curSize > maxSize:
                qprobe += 1
                compress.compress(srcFile, tmpFile, method, qprobe)
                curSize = os.path.getsize(tmpFile)
                #print str(qprobe)

           # print "Detailed " + str(curSize) + " probe " + str(qprobe)
            return qprobe # optimal parameter


        compress.compress(srcFile, tmpFile, method, qprobe)
        curSize = os.path.getsize(tmpFile)


        if curSize > maxSize:
           return actuallyFind(srcFile,maxSize,method,qprobe,maxQ)
        else:
            return actuallyFind(srcFile,maxSize,method,minQ,qprobe)


    else:
        print "ERROR: Invalid method " + method
        exit(-1)

def findOptimalSize(srcFile, upperBorderValue, method):

    maxSize = upperBorderValue
    #print maxSize

    if method == "jpg":
       minQ = 1
       maxQ = 100
    else:
        if method == "jxr":
           minQ = 1
           maxQ = 255
        else:
            if method=="jp2":
                minQ = 1
                maxQ = 100
            else:
                print "ERROR: Invalid method: " + method
                exit(-1)


    bestSingleQ = actuallyFind(srcFile, maxSize, method, minQ, maxQ)

    #print "best is " + str(bestSingleQ)
    return bestSingleQ



srcFolder="/home/tbergmueller/dev/mm/databases/iitd/"
dstFolder="/home/tbergmueller/dev/mm/databases_compressed/iitd/"
preCompFolder=dstFolder + "../precompress/";

methods=['jp2']
qp=[70,75,80,100]
#crs=[15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
crs=[65, 70, 75]
#crs = [20]
#shutil.rmtree(preCompFolder, 1)
#precompress(srcFolder, preCompFolder, qp)



for m in methods:
    #shutil.rmtree(dstFolder + "/method_" + m , 1)
    for crt in crs:
        singleFolderName = dstFolder + "/method_" + m + "/single/cr" + str(crt)+ "/"
        compress.mkdir_p(singleFolderName)

        for q in qp:
            doubleFolderName=dstFolder + "/method_" + m + "/double/cr" + str(crt) + "/quality" + str(q) + "/"
            compress.mkdir_p(doubleFolderName)

        for f in os.listdir(srcFolder):
            if not f.endswith(".bmp"):
                continue

            ssize = os.path.getsize(srcFolder + "/" + f) / crt
            bestQ = findOptimalSize(srcFolder + "/" + f, ssize, m)


            #write single compressed file
            singleFile = compress.compress(srcFolder + f, singleFolderName + f, m, bestQ)
            singleSize = os.path.getsize(singleFile)
            print "method " + m + " and CR=" + str(crt) + " .... " + f + " bestQ: " + str(bestQ) + " s(Is)=" + str(singleSize)


            for q in qp:
                inFile = preCompFolder + "/quality" + str(q) + "/" + f.replace(".bmp", ".jpg");
                outFile = dstFolder + "/method_" + m + "/double/cr" + str(crt) + "/quality" + str(q) + "/" + f

                bestQ = findOptimalSize(inFile, singleSize, m)
                #print bestQ
                writtenFile = compress.compress(inFile, outFile, m, bestQ)

                curSize = os.path.getsize(writtenFile)
                #print "size is " + str(curSize)

                if curSize > singleSize:
                    print "ERROR: Violating condition"
                   # exit(-1)



                #print writtenFile + " .... " + str(os.path.getsize(writtenFile))
