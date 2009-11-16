#!/usr/bin/python

import sys, struct
import zipfile
from cStringIO import StringIO

def read(file):
    """
    Return a generator that yields (url, data) tuples.
    """
    # Make sure "h" fmt returns 32-bits (hopefully an integer)
    assert(struct.calcsize("i")) == 4

    l = file.read(2*4)
    (classID, versionID) = struct.unpack("ii", l)
    # Current hard-coded values in http://code.google.com/p/eightylegs/source/browse/trunk/80legsCustomerResults/src/com/eightylegs/customer/job/CustomerResults.java
    assert (classID, versionID) == (218217067, 1)

    l = "not EOF"
    data = []
    l = file.read(1*4)
    while l != "":
        (URLSIZE,) = struct.unpack("i", l)
        url = file.read(URLSIZE).decode("utf-8")
#        print url.encode("utf-8")
        l = file.read(1*4)
        (DATASIZE,) = struct.unpack("i", l)
#        print DATASIZE
        data = str(file.read(DATASIZE))
        yield (url, data)
#        print data
#        print data.decode("utf-8")
        l = file.read(1*4)

def readzip(zfilename):
    """
    Read a zipfile and process all .80 files therein.
    """
    zfile = zipfile.ZipFile(zfilename, "r")
    for info in zfile.infolist():
        fname = info.filename
        if fname.endswith(".80"):
            data = zfile.read(fname)
            for r in read(StringIO(data)):
                yield r


if __name__ == "__main__":
    i = 0
    for url, data in read(sys.stdin):
        print url
        i += 1
        f = open("in3/%d.html" % i, "w")
        f.write(data)
#        print url, data
#        print url, len(data)
#        print len(data)
