plsGrab is a simple utility for extracting streaming URLs from either .pls files,
or web pages that reference .pls files.

It's implemented in Python 3, and tested under 3.4.2.

usage: ./plsGrab.py URL

The URL can either be a .pls file, in which case it extracts the first streaming URL from the file,
or an arbitrary URL, in which case the file will be searched for references to .pls files,
which will then be searched for the first streaming URL.

The program makes use of a shell variable DEBUG - if set to 1 or 2, different amounts of information
will be written to stderr as it searches.


