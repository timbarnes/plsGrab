#!/usr/bin/python -tt

# Read in a .pls file from the Internet, and print out the URL of the stream for mpd

import sys, os
import urllib, urllib2
from re import sub, search, findall


# Get the value of an external DEBUG shell variable to determine if we should print debug info
DebugMode = int(os.environ["DEBUG"])

def DEBUG(level, string, object):
    """Print debug information if the debug level is set"""
    
    if DebugMode >= level:
        print string, ':', object
    return

def getOneStreamURL(URL):
    """Extracts the first stream URL from the given .pls file"""
    
    DEBUG(1, 'getOneStreamURL looking for', URL)
    try:
        response = urllib2.urlopen(URL)
        html = response.read()
        DEBUG(2, 'plsStream HTML', html)
        stream = search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html)
        DEBUG(1, 'getOneStreamURL found', stream.group())
        if stream:
            stream = sub(r'(&|\?).*', '', stream.group())
            DEBUG(1, 'returning', stream)
            return stream
        DEBUG(1, 'getOneStreamURL', 'not found')
    except urllib2.URLError as e:
        print e.reason
    return


def getStreamURLs(URL):
    """If given a .pls URL, use regex to extract the URL up to the ? or end, whichever happens first.
    If a non-pls file, search the file for .pls entries, and process each."""

    responseList = []
    if URL[-4:] == '.pls':
        DEBUG(1, 'Single Pls', URL)
        responseList.append(getOneStreamURL(URL))
        DEBUG(1, 'getStreamURLs found', responseList)
        return responseList
    else:
        DEBUG(1, 'getStreamURLs looking for multiple in', URL)
        try:
            response = urllib2.urlopen(URL)
            html = response.read()
            plsURLs = findall(r'(http://.*\.pls)', html)
            DEBUG(1, 'getStreamURLs found:', plsURLs)
            for plsURL in plsURLs:
                DEBUG(1, 'getStreamURLs looking for', plsURL)
                plsURL = sub(r'.pls.*', '.pls', plsURL)
                streamURL = getOneStreamURL(plsURL)
                if streamURL:
                    responseList.append(streamURL)
            return responseList
        except urllib2.URLError as e:
            print e.reason
    return
    

def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: URL'
        sys.exit(1)

    for arg in args:
        DEBUG(1, 'main', args)
        URLs = getStreamURLs(arg)
        DEBUG(1, 'main result', URLs)
        for URL in URLs:
            print URL
        
if __name__ == '__main__':
  main()
