__author__ = 'tbergmueller'

# /home/tberg/mmFormats/results/iitd/method_jp2/double/caht/cr15/quality70

import os
import errno
from shutil import copyfile




def excerptCSVs(folderFrom, folderTo):


    data = {}


    for dirname, dirnames, filenames in os.walk(folderFrom):

        # print path to all filenames.
        for filename in filenames:

            if filename.endswith('.csv') and not filename.endswith('.dist.csv'):
               fullFilename = os.path.join(dirname, filename)
               fullTarget = fullFilename.replace(folderFrom, folderTo)
               print(fullFilename + '\t->\t' + fullTarget)

               try:

                   if not os.path.exists(fullTarget.replace(filename, '')):
                       os.makedirs(fullTarget.replace(filename, ''))

                   copyfile(fullFilename, fullTarget)

               except OSError as exc:
                   if exc.errno == errno.EEXIST and os.path.isdir(fullTarget):
                       pass
                   else:
                       raise
