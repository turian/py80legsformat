#!/usr/bin/python

import sys, struct

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

if __name__ == "__main__":
    for url, data in read(sys.stdin):
        print url
#        print url, data
#        print url, len(data)
#        print len(data)
