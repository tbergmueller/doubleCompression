from PIL import Image, ImageDraw
import subprocess
import os, errno


def saveAsJPG(srcFile, path, q):
    img = Image.open(srcFile);
    outfile =  path.replace(os.path.splitext(path)[1], ".jpg")
    img.save(outfile, 'JPEG', quality=q)
    return outfile

def saveAsJ2k(srcFile, path, q):
    img = Image.open(srcFile);

    outfile =  path.replace(os.path.splitext(path)[1], ".jp2")

    img.save(outfile, 'JPEG2000', quality_mode="rates", quality_layers=[50], )
    return outfile


def saveAsJXR(srcFile, path, q):

    if os.path.splitext(srcFile)[1] == ".jpg":
        img = Image.open(srcFile)
        img.save("hugo.bmp")

    srcFile = "hugo.bmp"

    outfile = path.replace(os.path.splitext(path)[1], ".jxr")
    command = "./JxrEncApp -i " + srcFile + " -o " + outfile + " -q " + str(q)

    status = subprocess.call(command.split(), shell=False)
    return outfile

def compress(srcFile, path, method, q):
    if method == "jpg":
        return saveAsJPG(srcFile,path,q)
    else:
        if method == "jxr":
            return saveAsJXR(srcFile,path,q)
        else:
            if method == "jp2":
                return saveAsJ2k(srcFile,path,q)
            else:
                print("ERROR: unknown compression method");
                exit(-1);



def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise




