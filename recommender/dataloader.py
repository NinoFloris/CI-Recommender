# External imports #
import cPickle
import bz2


"""
    This function loads the datasets, if trybz2 is true it also searches for .bz2 files
    However that is not recommended, extract these .bz2 files once and keep them in your local repo
    The loading times decrease by a factor 10 at least
    .gitignore has excluded these extracted files so they won't get uploaded
"""


def load(path, trybz2=True):
    if path.exists(path):
        try:
            return cPickle.load(open(path, 'rb'))
        except IOError:
            raise
    elif trybz2 and path.exists(path + '.bz2'):
        try:
            return cPickle.load(bz2.BZ2File(path+'.bz2', 'rb'))
        except IOError:
            raise
