__author__ = 'tbergmueller'
# Path structure
# /home/tberg/mmFormats/results/iitd/method_jp2/double/caht/cr15/quality70

from excerptCSVs import excerptCSVs


skimThrough='/home/tbergmueller/DEV/doubleCompression/doubleCompression/results/mser/rawResults/'
putTo = '/tmp/test/'


data = excerptCSVs(skimThrough, putTo)
